from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Sum
from accounts.models import User
from books.models import Book, Purchase, Review


@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        return redirect('book_list')

    sales = Purchase.objects.filter(seller=request.user).select_related('book', 'buyer').order_by('-sale_date')

    total_revenue = sales.aggregate(Sum('sale_price'))['sale_price__sum'] or 0
    books_sold_count = sales.count()
    active_ads_count = Book.objects.filter(seller=request.user, is_sold=False).count()

    avg_rating = Review.objects.filter(book__seller=request.user).aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, 'stats/seller_dashboard.html', {
        'sales': sales,
        'total_revenue': total_revenue,
        'books_sold_count': books_sold_count,
        'active_ads_count': active_ads_count,
        'avg_rating': round(avg_rating, 1)
    })

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()

    total_sales_data = Purchase.objects.aggregate(total=Sum('sale_price'))
    total_sales_volume = total_sales_data['total'] or 0

    total_books_listed = Book.objects.count()
    active_listings = Book.objects.filter(is_sold=False).count()

    context = {
        'total_users': total_users,
        'total_sales_volume': total_sales_volume,
        'total_books_listed': total_books_listed,
        'active_listings': active_listings,
    }
    return render(request, 'stats/admin_dashboard.html', context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from accounts.models import User
from books.models import Book, Purchase

@login_required
def seller_dashboard(request):
    earnings_data = Purchase.objects.filter(seller=request.user).aggregate(total=Sum('sale_price'))
    total_earned = earnings_data['total'] or 0

    books_sold = Purchase.objects.filter(seller=request.user).count()

    active_books = Book.objects.filter(seller=request.user, is_sold=False).count()

    sales_history = Purchase.objects.filter(seller=request.user).order_by('-sale_date')

    context = {
        'total_earned': total_earned,
        'books_sold': books_sold,
        'active_books': active_books,
        'sales_history': sales_history,
    }
    return render(request, 'stats/seller_dashboard.html', context)


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
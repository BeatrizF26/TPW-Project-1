from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg, Sum
from accounts.models import User
from accounts.decorators import seller_required
from books.models import Book, Purchase, Review


@seller_required
def seller_dashboard(request):
    status_filter = request.GET.get('status')
    if status_filter not in {'sold', 'active', 'disabled'}:
        status_filter = 'sold'

    sales = Purchase.objects.filter(seller=request.user).select_related('book', 'buyer').order_by('-sale_date')
    seller_books = Book.objects.filter(seller=request.user).select_related('purchase__buyer').order_by('-created_at')

    total_revenue = sales.aggregate(Sum('sale_price'))['sale_price__sum'] or 0
    books_sold_count = sales.count()
    active_ads_count = Book.objects.filter(seller=request.user, is_sold=False, is_active=True).count()
    disabled_ads_count = Book.objects.filter(seller=request.user, is_sold=False, is_active=False).count()

    avg_rating = Review.objects.filter(book__seller=request.user).aggregate(Avg('rating'))['rating__avg'] or 0

    if status_filter == 'active':
        dashboard_items = seller_books.filter(is_sold=False, is_active=True)
    elif status_filter == 'disabled':
        dashboard_items = seller_books.filter(is_sold=False, is_active=False)
    else:
        dashboard_items = sales

    return render(request, 'stats/seller_dashboard.html', {
        'sales': sales,
        'dashboard_items': dashboard_items,
        'status_filter': status_filter,
        'total_revenue': total_revenue,
        'books_sold_count': books_sold_count,
        'active_ads_count': active_ads_count,
        'disabled_ads_count': disabled_ads_count,
        'avg_rating': round(avg_rating, 1)
    })

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    from django.db.models import Count, Avg, Sum
    from django.db.models.functions import TruncMonth

    users = User.objects.order_by('-date_joined').annotate(
        avg_rating=Avg('book__review__rating')
    )

    total_users    = users.count()
    buyer_count    = users.filter(is_buyer=True).count()
    seller_count   = users.filter(is_seller=True).count()
    both_count     = users.filter(is_buyer=True, is_seller=True).count()
    admin_count    = users.filter(is_staff=True).count()

    total_books    = Book.objects.count()
    active_books   = Book.objects.filter(is_sold=False, is_active=True).count()
    sold_books     = Book.objects.filter(is_sold=True).count()
    disabled_books = Book.objects.filter(is_sold=False, is_active=False).count()

    total_purchases   = Purchase.objects.count()
    total_revenue     = Purchase.objects.aggregate(t=Sum('sale_price'))['t'] or 0
    avg_sale_price    = Purchase.objects.aggregate(a=Avg('sale_price'))['a'] or 0
    total_reviews     = Review.objects.count()
    avg_review_rating = Review.objects.aggregate(a=Avg('rating'))['a'] or 0

    top_sellers = (
        Purchase.objects
        .values('seller__username')
        .annotate(revenue=Sum('sale_price'), sales=Count('id'))
        .order_by('-revenue')[:5]
    )

    top_buyers = (
        Purchase.objects
        .values('buyer__username')
        .annotate(spent=Sum('sale_price'), purchases=Count('id'))
        .order_by('-spent')[:5]
    )

    # monthly sales for line chart (last 6 months)
    monthly_sales = (
        Purchase.objects
        .annotate(month=TruncMonth('sale_date'))
        .values('month')
        .annotate(count=Count('id'), revenue=Sum('sale_price'))
        .order_by('month')
    )
    monthly_labels = [m['month'].strftime('%b %Y') for m in monthly_sales]
    monthly_counts = [m['count'] for m in monthly_sales]
    monthly_revenues = [float(m['revenue']) for m in monthly_sales]

    # books by genre for doughnut chart
    genre_data = (
        Book.objects
        .values('genre')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    genre_labels = [g['genre'] for g in genre_data]
    genre_counts = [g['count'] for g in genre_data]

    context = {
        'users': users,
        'total_users': total_users,
        'buyer_count': buyer_count,
        'seller_count': seller_count,
        'both_count': both_count,
        'admin_count': admin_count,
        'total_books': total_books,
        'active_books': active_books,
        'sold_books': sold_books,
        'disabled_books': disabled_books,
        'total_purchases': total_purchases,
        'total_revenue': total_revenue,
        'avg_sale_price': round(avg_sale_price, 2),
        'total_reviews': total_reviews,
        'avg_review_rating': round(avg_review_rating, 1),
        'top_sellers': top_sellers,
        'top_buyers': top_buyers,
        'monthly_labels': monthly_labels,
        'monthly_counts': monthly_counts,
        'monthly_revenues': monthly_revenues,
        'genre_labels': genre_labels,
        'genre_counts': genre_counts,
    }
    return render(request, 'stats/admin_dashboard.html', context)

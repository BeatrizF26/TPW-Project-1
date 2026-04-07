# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import buyer_required, seller_required
from accounts.mode import SELLER_MODE, get_active_mode
from .models import Book, Purchase, Review, Favorite
from django.contrib import messages
from django.db.models import Count, Q, Sum, F

@login_required
def book_list(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    active_mode = get_active_mode(request)
    seller_stats = None
    seller_sort = request.GET.get('sort')
    if active_mode == SELLER_MODE:
        books = Book.objects.filter(seller=request.user).annotate(
            favorites_count=Count('favorites', distinct=True),
        )
        seller_stats = {
            'total': books.count(),
            'live': books.filter(is_active=True, is_sold=False).count(),
            'sold': books.filter(is_sold=True).count(),
            'inactive': books.filter(is_active=False, is_sold=False).count(),
            'views': books.aggregate(total=Sum('view_count'))['total'] or 0,
        }
    else:
        books = Book.objects.filter(is_sold=False, is_active=True).annotate(
            favorites_count=Count('favorites', distinct=True)
        ).order_by('-created_at')
        if request.user.is_authenticated:
            books = books.exclude(seller=request.user)

    query = request.GET.get('q')
    genre = request.GET.get('genre')
    max_price = request.GET.get('max_price')

    if query:
        books = books.filter(title__icontains=query)

    if genre:
        books = books.filter(genre=genre)

    if max_price:
        try:
            books = books.filter(price__lte=max_price)
        except ValueError:
            pass

    if active_mode == SELLER_MODE:
        if seller_sort == 'views':
            books = books.order_by('-view_count', '-created_at')
        elif seller_sort == 'saved':
            books = books.order_by('-favorites_count', '-view_count', '-created_at')
        else:
            books = books.order_by('-created_at')

    return render(request, 'books/list.html', {
        'books': books,
        'query_params': request.GET,
        'active_mode': active_mode,
        'genre_choices': Book.GENRES,
        'seller_stats': seller_stats,
        'seller_sort': seller_sort or '',
    })

@login_required
@seller_required
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.is_active = True
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'books/create.html', {'form': form})


@login_required
@seller_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, seller=request.user)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, 'books/create.html', {
        'form': form,
        'is_edit_mode': True,
        'book': book,
    })


@login_required
@buyer_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.is_sold:
        messages.error(request, "This book is not available.")
        return redirect('book_list')

    if book.seller == request.user:
        messages.error(request, "You can't buy your own book.")
        return redirect('book_list')

    Purchase.objects.create(
        book=book,
        buyer=request.user,
        seller=book.seller,
        sale_price=book.price
    )

    book.is_sold = True
    book.save()

    messages.success(request, f"Success! You bought '{book.title}'.")
    return redirect('book_list')

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_favorite = False

    should_count_view = not request.user.is_authenticated or request.user != book.seller

    if should_count_view:
        Book.objects.filter(id=book.id).update(view_count=F('view_count') + 1)
        book.refresh_from_db(fields=['view_count'])

    if request.user.is_authenticated and request.user != book.seller:
        is_favorite = Favorite.objects.filter(book=book, user=request.user).exists()

    return render(request, 'books/detail.html', {
        'book': book,
        'is_favorite': is_favorite,
        'favorites_count': book.favorites.count(),
    })


@login_required
@seller_required
def toggle_book_status(request, book_id):
    book = get_object_or_404(Book, id=book_id, seller=request.user)

    if request.method == 'POST' and not book.is_sold:
        book.is_active = not book.is_active
        book.save(update_fields=['is_active'])

    return redirect('book_detail', book_id=book.id)


@login_required
@seller_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, seller=request.user)

    if request.method == 'POST' and not book.is_sold:
        book.delete()
        return redirect('book_list')

    return redirect('book_detail', book_id=book.id)


@login_required
@buyer_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_active=True, is_sold=False)

    if book.seller == request.user:
        return redirect('book_detail', book_id=book.id)

    if request.method == 'POST':
        favorite, created = Favorite.objects.get_or_create(book=book, user=request.user)
        if not created:
            favorite.delete()

    return redirect('book_detail', book_id=book.id)


@login_required
@buyer_required
def remove_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        Favorite.objects.filter(book=book, user=request.user).delete()
    return redirect('my_favorites')


@login_required
@buyer_required
def my_purchases(request):
    purchases = Purchase.objects.filter(buyer=request.user).select_related('book').order_by('-sale_date')
    return render(request, 'books/purchases.html', {'purchases': purchases})


@login_required
@buyer_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book', 'book__seller').order_by('-created_at')
    return render(request, 'books/favorites.html', {'favorites': favorites})


@login_required
@buyer_required
def confirm_purchase(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_sold=False, is_active=True)

    if request.method == 'POST':
        book.is_sold = True
        book.save()

        Purchase.objects.create(
            book=book,
            buyer=request.user,
            seller=book.seller,
            sale_price=book.price
        )

        messages.success(request, f"You successfully bought '{book.title}'!")
        return redirect('my_purchases')

    return render(request, 'books/confirm_purchase.html', {'book': book})


@login_required
@buyer_required
def leave_review(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_sold=True)

    if not Purchase.objects.filter(book=book, buyer=request.user).exists():
        messages.error(request, "You can only review books you have purchased.")
        return redirect('my_purchases')

    review = Review.objects.filter(book=book, buyer=request.user).first()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.update_or_create(
            book=book,
            buyer=request.user,
            defaults={
                'rating': rating,
                'comment': comment
            }
        )
        return redirect('my_purchases')

    return render(request, 'books/reviews.html', {
        'book': book,
        'review': review
    })

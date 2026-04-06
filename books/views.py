# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import buyer_required, seller_required
from accounts.mode import SELLER_MODE, get_active_mode
from .models import Book, Purchase, Review
from django.contrib import messages

@login_required
def book_list(request):
    active_mode = get_active_mode(request)
    if active_mode == SELLER_MODE:
        books = Book.objects.filter(seller=request.user).order_by('-created_at')
    else:
        books = Book.objects.filter(is_sold=False, is_active=True)
        if request.user.is_authenticated:
            books = books.exclude(seller=request.user)

    query = request.GET.get('q')
    genre = request.GET.get('genre')
    max_price = request.GET.get('max_price')

    if query:
        books = books.filter(title__icontains=query)

    if genre:
        books = books.filter(genre__icontains=genre)

    if max_price:
        try:
            books = books.filter(price__lte=max_price)
        except ValueError:
            pass

    return render(request, 'books/list.html', {
        'books': books,
        'query_params': request.GET,
        'active_mode': active_mode,
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
    return render(request, 'books/detail.html', {'book': book})


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
def my_purchases(request):
    purchases = Purchase.objects.filter(buyer=request.user).select_related('book').order_by('-sale_date')
    return render(request, 'books/purchases.html', {'purchases': purchases})


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

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm
from django.contrib.auth.decorators import login_required
from .models import Book, Purchase
from django.contrib import messages

def book_list(request):
    books = Book.objects.filter(is_sold=False)

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
        'query_params': request.GET
    })

@login_required
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'books/create.html', {'form': form})


@login_required
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
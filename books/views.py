# Create your views here.
from .models import Book
from django.shortcuts import render, redirect
from .forms import BookForm
from django.contrib.auth.decorators import login_required

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})

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
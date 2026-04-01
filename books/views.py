from django.shortcuts import render

# Create your views here.
from .models import Book
from django.shortcuts import render, redirect
from .forms import BookForm
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'books/create.html', {'form': form})
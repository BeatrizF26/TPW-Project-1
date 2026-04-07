from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'price', 'description', 'condition', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. The Great Gatsby'}),
            'author': forms.TextInput(attrs={'placeholder': 'e.g. F. Scott Fitzgerald'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the book, edition, notes, or anything a buyer should know.'}),
            'image': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].choices = [('', 'Select a genre')] + list(Book.GENRES)
        self.fields['condition'].choices = [('', 'Select the condition')] + list(Book.CONDITIONS)

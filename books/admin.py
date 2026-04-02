from django.contrib import admin
from .models import Book, Purchase

admin.site.register(Book)
admin.site.register(Purchase)
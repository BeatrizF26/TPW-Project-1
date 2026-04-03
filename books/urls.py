from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.create_book, name='create_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('buy/<int:book_id>/', views.buy_book, name='buy_book'),
]
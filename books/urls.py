from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.book_list, name='book_list'),
    path('create/', views.create_book, name='create_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/toggle-status/', views.toggle_book_status, name='toggle_book_status'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('buy/<int:book_id>/', views.buy_book, name='buy_book'),
    path('my-purchases/', views.my_purchases, name='my_purchases'),
    path('confirm-purchase/<int:book_id>/', views.confirm_purchase, name='confirm_purchase'),
    path('leave-review/<int:book_id>/', views.leave_review, name='leave_review'),
]

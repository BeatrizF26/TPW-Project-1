from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:book_id>/', views.start_conversation, name='start_conversation'),
    path('inbox/', views.inbox, name='inbox'),
    path('view/<int:chat_id>/', views.view_chat, name='view_chat'),
    path('delete/<int:chat_id>/', views.delete_chat, name='delete_chat'), 
]
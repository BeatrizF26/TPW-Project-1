from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('admin-stats/', views.admin_dashboard, name='admin_dashboard'),
]
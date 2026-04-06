from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            authentication_form=CustomAuthenticationForm,
        ),
        name='login',
    ),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/upgrade-seller/', views.upgrade_to_seller, name='upgrade_to_seller'),
    path('profile/upgrade-buyer/', views.upgrade_to_buyer, name='upgrade_to_buyer'),
    path('switch-mode/', views.toggle_account_mode, name='toggle_account_mode'),
]

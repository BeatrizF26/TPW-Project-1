from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
from .forms import CustomAuthenticationForm


class SmartLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return '/stats/admin-stats/'
        return str(reverse_lazy('book_list'))


urlpatterns = [
    path('login/', SmartLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('users/<str:username>/', views.public_profile, name='public_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/upgrade-seller/', views.upgrade_to_seller, name='upgrade_to_seller'),
    path('profile/upgrade-buyer/', views.upgrade_to_buyer, name='upgrade_to_buyer'),
    path('switch-mode/', views.toggle_account_mode, name='toggle_account_mode'),
]

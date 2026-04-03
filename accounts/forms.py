from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, BuyerProfile, SellerProfile

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_seller']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BuyerProfileEditForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['address', 'favorite_genres']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'favorite_genres': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SellerProfileEditForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['iban']
        widgets = {
            'iban': forms.TextInput(attrs={'class': 'form-control'}),
        }
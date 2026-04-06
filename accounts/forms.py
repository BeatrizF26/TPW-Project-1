from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, BuyerProfile, SellerProfile


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': 'Invalid username or password.',
    }

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial='buyer',
        label='Start as'
    )

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        user.is_buyer = role == 'buyer'
        user.is_seller = role == 'seller'

        if commit:
            user.save()
        return user


class SellerUpgradeForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['iban']
        widgets = {
            'iban': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PT50 0002 0123 1234 5678 9015 4'}),
        }

class UserEditForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }


class BuyerProfileEditForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['address', 'favorite_genres']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Shipping address'}),
            'favorite_genres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fantasy, Mystery, Romance...'}),
        }


class SellerProfileEditForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['iban']
        widgets = {
            'iban': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PT50 0002 0123 1234 5678 9015 4'}),
        }

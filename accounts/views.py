from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserEditForm, BuyerProfileEditForm, SellerProfileEditForm
from django.contrib.auth.decorators import login_required
from books.models import Purchase

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    my_purchases = Purchase.objects.filter(buyer=request.user).order_by('-sale_date')

    context = {
        'user': request.user,
        'my_purchases': my_purchases
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    buyer_profile = user.buyer_profile
    seller_profile = user.seller_profile

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        buyer_form = BuyerProfileEditForm(request.POST, instance=buyer_profile)
        seller_form = SellerProfileEditForm(request.POST, instance=seller_profile)

        if user_form.is_valid() and buyer_form.is_valid() and seller_form.is_valid():
            user_form.save()
            buyer_form.save()
            seller_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=user)
        buyer_form = BuyerProfileEditForm(instance=buyer_profile)
        seller_form = SellerProfileEditForm(instance=seller_profile)

    context = {
        'user_form': user_form,
        'buyer_form': buyer_form,
        'seller_form': seller_form,
    }
    return render(request, 'accounts/edit_profile.html', context)
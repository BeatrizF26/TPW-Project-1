from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from books.models import Purchase
from .mode import BUYER_MODE, SELLER_MODE, get_active_mode, set_active_mode
from .forms import (
    RegisterForm,
    UserEditForm,
    BuyerProfileEditForm,
    SellerProfileEditForm,
    SellerUpgradeForm,
)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            set_active_mode(request, SELLER_MODE if user.is_seller else BUYER_MODE)

            return redirect('book_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    my_purchases = Purchase.objects.filter(buyer=request.user).order_by('-sale_date')

    context = {
        'user': request.user,
        'my_purchases': my_purchases,
        'active_mode': get_active_mode(request),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def upgrade_to_seller(request):
    if request.user.is_seller:
        return redirect('profile')

    seller_profile = request.user.seller_profile

    if request.method == 'POST':
        form = SellerUpgradeForm(request.POST, instance=seller_profile)
        if form.is_valid():
            form.save()
            request.user.is_seller = True
            request.user.save(update_fields=['is_seller'])
            set_active_mode(request, SELLER_MODE)
            return redirect('profile')
    else:
        form = SellerUpgradeForm(instance=seller_profile)

    return render(request, 'accounts/upgrade_seller.html', {'form': form})


@login_required
def upgrade_to_buyer(request):
    if request.user.is_buyer:
        return redirect('profile')

    if request.method == 'POST':
        request.user.is_buyer = True
        request.user.save(update_fields=['is_buyer'])
        set_active_mode(request, BUYER_MODE)
        return redirect('profile')

    return render(request, 'accounts/upgrade_buyer.html')


@login_required
def toggle_account_mode(request):
    if not (request.user.is_buyer and request.user.is_seller):
        return redirect('profile')

    current_mode = get_active_mode(request)
    next_mode = BUYER_MODE if current_mode == SELLER_MODE else SELLER_MODE
    set_active_mode(request, next_mode)
    return redirect('book_list')

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

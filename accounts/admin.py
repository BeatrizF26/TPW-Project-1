from django.contrib import admin
from .models import User, BuyerProfile, SellerProfile

admin.site.register(User)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)

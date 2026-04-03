from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.username

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    address = models.TextField(blank=True, null=True)
    favorite_genres = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Buyer Profile: {self.user.username}"

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    iban = models.CharField(max_length=34, blank=True, null=True)
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Seller Profile: {self.user.username}"

@receiver(post_save, sender=User)
def manage_user_profiles(sender, instance, created, **kwargs):
    if created:
        BuyerProfile.objects.create(user=instance)
        SellerProfile.objects.create(user=instance)
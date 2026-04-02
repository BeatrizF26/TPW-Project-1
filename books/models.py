from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Book(models.Model):
    CONDITIONS = [
        ('NEW', 'New'),
        ('LIKE NEW', 'Like New'),
        ('ACCEPTABLE', 'Acceptable'),
        ('OLD', 'Old')
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(choices=CONDITIONS, default='ACCEPTABLE')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return self.title

class Purchase(models.Model):
    STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]

    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='purchase')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} bought by {self.buyer.username}"
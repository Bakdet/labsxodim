from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='item_pictures/')
    description = models.CharField(max_length=300, default=None, blank=True, null=True)
    id=models.AutoField(primary_key=True)
    @staticmethod
    def search(query, min_price=None, max_price=None):
        items = Item.objects.filter(name__icontains=query)
        if min_price:
            items = items.filter(price__gte=min_price)
        if max_price:
            items = items.filter(price__lte=max_price)
        return items
    def str(self):
        return self.name
class ItemRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300, default=None, blank=True, null=True)
    picture = models.ImageField(upload_to='item_pictures/')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='item_pictures', blank=True, null=True)
    id=models.AutoField(primary_key=True)
    def __str__(self):
        return f'{self.user.username} Profile'

# Create your models ere.

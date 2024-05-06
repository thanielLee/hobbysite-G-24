from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from user_management.models import Profile

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    producttype = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_sale', 'On Sale'),
        ('out_of_stock', 'Out of Stock'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status = 'out_of_stock'
        super().save(*args, **kwargs)

class Transaction(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    STATUS_CHOICES = [
        ('on_cart', 'On Cart'),
        ('to_pay', 'To Pay'),
        ('to_ship', 'To Ship'),
        ('to_receive', 'To Receive'),
        ('delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
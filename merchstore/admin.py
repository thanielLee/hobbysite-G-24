from django.contrib import admin
from .models import ProductType, Product, Transaction, Profile

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'producttype', 'owner', 'price', 'stock', 'status']
    list_filter = ['producttype', 'status']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'product', 'amount', 'status', 'created_on']
    list_filter = ['status', 'created_on']
    search_fields = ['product__name', 'buyer__user__username']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
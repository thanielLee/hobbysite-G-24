from django.contrib import admin

from .models import Product, ProductType, Transaction


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType


class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ["name", "price", "type"]
    list_filter = ["type"]
    search_fields = ["name"]


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
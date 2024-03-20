from django.contrib import admin

from merchstore.models import Product, ProductType


class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name', 'description', 'price', 'producttype', ]

class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    search_fields = ('name', )
    list_display = ('name', 'description', 'id', )
    list_filter = ('name', )
    inlines = [ProductInline, ]

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'description', 'price', 'producttype')

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
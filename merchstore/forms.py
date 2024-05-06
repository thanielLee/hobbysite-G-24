from django import forms
from .models import Transaction, Product

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'amount']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'producttype', 'description', 'price', 'stock', 'status']
        widgets = {
            'status': forms.Select(choices=Product.STATUS_CHOICES),
            'producttype': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

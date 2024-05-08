from typing import Any

from django import forms

from user_management.models import Profile

from .models import Product, Transaction


class ProductForm(forms.ModelForm):

    owner = forms.ModelChoiceField(required=False, queryset=Profile.objects)

    class Meta:
        model = Product
        fields = "__all__"


class TransactionForm(forms.ModelForm):
    amount = forms.IntegerField(min_value=0)

    class Meta:
        model = Transaction
        fields = ['amount']
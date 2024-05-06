from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, CartView, TransactionsListView
)

urlpatterns = [
    path('items/', ProductListView.as_view(), name='product_list'),
    path('item/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('item/add/', ProductCreateView.as_view(), name='product_create'),
    path('item/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('transactions/', TransactionsListView.as_view(), name='transactions_list'),
]

app_name = 'merchstore'

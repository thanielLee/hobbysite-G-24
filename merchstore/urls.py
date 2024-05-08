from django.urls import path

from .views import (
    CartView,
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    TransactionListView,
)

urlpatterns = [
    path("items/", ProductListView.as_view(), name="product_list"),
    path("item/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("item/add/", ProductCreateView.as_view(), name="product_create"),
    path("item/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("cart/", CartView.as_view(), name="cart"),
    path(
        "transactions/",
        TransactionListView.as_view(),
        name="transaction_list",
    ),
]

app_name = "merchstore"
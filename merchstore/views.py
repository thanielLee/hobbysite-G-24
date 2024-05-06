from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Transaction
from .forms import TransactionForm, ProductForm

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'merchstore_product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_products'] = Product.objects.filter(owner=self.request.user.Profile)
        context['other_products'] = Product.objects.exclude(owner=self.request.user.Profile)
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'merchstore_product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = Product.objects.get(id=self.kwargs["pk"])
        context['form'] = TransactionForm(initial={'product': object})
        context['is_owner'] = object.owner == self.request.user.Profile
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.get_context_data()['is_owner']:
            form = TransactionForm(data = request.POST)
            if form.is_valid():
                form.instance.buyer = request.user.Profile
                form.save()
                return redirect('merchstore:cart_view')
        return redirect('merchstore:product_detail', pk=self.kwargs['pk'])

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'merchstore_product_form.html'
    success_url = reverse_lazy('merchstore:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user.Profile
        form.is_valid()
        form.save()
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'merchstore_product_form.html'
    success_url = reverse_lazy('merchstore:product_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user.Profile)

class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore_cart.html'

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user.Profile)

class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore_transactions_list.html'

    def get_queryset(self):
        return Transaction.objects.filter(product__owner=self.request.user.Profile)
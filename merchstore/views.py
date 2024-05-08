from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse

from user_management.models import Profile
from .forms import ProductForm, TransactionForm
from .models import Product, ProductType, Transaction

class ProductListView(ListView):
    model = Product
    template_name = "merchstore_product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_types"] = ProductType.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore_product_type_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TransactionForm()
        form.fields["amount"].widget.attrs["max"] = context["product"].stock
        context["form"] = form
        return context
    
    def dispatch(self, request, *args, **kwargs):
        transaction_data = request.session.get('transaction_data')
        if transaction_data:
            new_form = TransactionForm()
            new_transaction = new_form.save(commit=False)
            user = self.request.user
            new_transaction.buyer = user.Profile
            new_transaction.amount = transaction_data['amount']
            product = Product.objects.get(id=transaction_data['product_id'])
            new_transaction.product = product
            product.stock -= transaction_data['amount']
            new_transaction.status = "On Cart"
            new_transaction.save()
            product.save()
            del request.session['transaction_data']
            return redirect("merchstore:cart")
        return super().dispatch(request, *args, **kwargs)




    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        product = self.get_object()
        form.is_valid()

        if not self.request.user.is_authenticated:
            print(product,  form.cleaned_data['amount'])
            request.session['transaction_data'] = {
                'product_id' : product.id,
                'amount' : form.cleaned_data['amount']
            }
            login_url = reverse('login') + '?next=' + request.get_full_path()
            return redirect(login_url)
        
        if form.is_valid():
            transaction = Transaction()
            transaction.product = product
            transaction.amount = form.cleaned_data["amount"]
            transaction.buyer = request.user.Profile
            transaction.status = "On_Cart"
            transaction.save()
            product.stock -= form.cleaned_data["amount"]
            product.save()
            return redirect("merchstore:cart")
        else:
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "merchstore_product_create.html"
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context["form"]
        form.fields["owner"].initial = Profile.objects.get(user=self.request.user)
        form.fields["owner"].disabled = True
        context["form"] = form
        return context

    def form_valid(self, form):
        form.instance.owner = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "merchstore_product_create.html"
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context["form"]
        form.fields["owner"].initial = Profile.objects.get(user=self.request.user)
        form.fields["owner"].disabled = True
        context["form"] = form
        return context

    def form_valid(self, form):
        if form.instance.stock == 0:  
            form.instance.status = "Out of Stock"
        print(self.request.POST)
        data = dict(self.request.POST)  
        form.instance.status = data['status'][0]
        form.instance.owner = Profile.objects.get(user=self.request.user)
        form.is_valid()
        form.save()
        return super().form_valid(form)

class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owners"] = Profile.objects.all()
        return context

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore_transactions_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buyers"] = Profile.objects.all()
        return context

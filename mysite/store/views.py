from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View, CreateView
from .utils import recalc_cart
from .mixins import CartMixin
from .models import Customer, Product, Category, Cart, CartProduct, Order
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomerForms, OrderForm, LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.db.models import Q


class LoginView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'category': categories, 'cart': self.cart}
        return render(request, 'store/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, "store/login.html", context)


class RegistrationView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'store/login.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'registration.html', context)


class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        categories = Category.objects.all()
        return render(request, 'store/profile.html', {'orders': orders, 'cart': self.cart, 'categories': categories})


class Home(CartMixin, ListView):                       # для главной страницы
    model = Product
    template_name = 'store/home.html'       # дефолтное название шаблона
    context_object_name = 'products'        # дефолтное название обьекта "Product"
    allow_empty = False                     # не показывать пустой список

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'SHOP'
        context['cart'] = self.cart
        return context

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category')


class ProductItem(CartMixin, DetailView):                  # для одного продукта
    model = Product
    template_name = 'store/product_item.html'   # дефолтное название шаблона
    context_object_name = 'news_item'           # дефолтное название обьекта "Product"
    slug_url_kwarg = 'slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context

    def get_queryset(self):         # создается объект типа queryset со списком объектов, которые можно обходить в цикле
        return Product.objects.filter(slug=self.kwargs['slug'], is_active=True)


class CategoryItem(CartMixin, ListView):               # для просмотра товаров одной категории
    template_name = 'store/category.html'   # дефолтное название шаблона
    context_object_name = 'categories'      # дефолтное название обьекта
    allow_empty = False                     # не показывать пустой список

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = Category.objects.get(slug=self.kwargs['slug'], is_active=True)
        context['cart'] = self.cart
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
        }
        return render(request, 'store/cart.html', context)


class AddToCartView(CartMixin, View):       # добавление товара в корзины

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class DeleteCartView(CartMixin, View):    # удаление товара из корзины

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product, product_id=product.id,
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ChangeQTY(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product, product_id=product.id,
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class Ordering(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form,
        }
        return render(request, 'store/ordering.html', context)


class MakeOrder(CartMixin, View):       # для обработки оформления заказа

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/ordering/')


class SearchView(CartMixin, ListView):
    """ поиск на сайте """
    model = Product
    template_name = 'store/product_list.html'  # дефолтное название шаблона
    context_object_name = 'products'  # дефолтное название обьекта "Product"
    allow_empty = False

    def get_queryset(self):
        query = self.request.GET.get('q')
        products = Product.objects.filter(
            Q(name__iregex=query)
        )
        return products
from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
from .views import LoginView,\
    Home, \
    ProductItem, \
    CategoryItem, \
    CartView, \
    AddToCartView, \
    DeleteCartView, \
    ChangeQTY, \
    Ordering, \
    MakeOrder, \
    RegistrationView, \
    ProfileView, \
    SearchView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', CategoryItem.as_view(), name='category'),
    path('product/<str:slug>/', ProductItem.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from/<str:slug>/', DeleteCartView.as_view(), name='delete_cart'),
    path('change-qty/<str:slug>/', ChangeQTY.as_view(), name='change_qty'),
    path('ordering/', Ordering.as_view(), name='ordering'),
    path('make-order/', MakeOrder.as_view(), name='make_order'),
    path('search/', SearchView.as_view(), name='search'),
]
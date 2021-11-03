from django.views.generic import View
from .models import Cart, Customer
from django.http import HttpResponseRedirect


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer,
                                       in_order=False).select_related('owner').prefetch_related('products').first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            # return HttpResponseRedirect('/login/')
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)

        self.cart = cart
        self.cart.save()
        return super().dispatch(request, *args, **kwargs)

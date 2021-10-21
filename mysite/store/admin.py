from django.contrib import admin
from store.models import Customer, Order, Product, Category, CartProduct, Cart


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'address']
    list_display_links = ['user']

    class Meta:
        model = Customer


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    list_display_links = ['customer']
    # inlines = [ProductInOrderInline]

    class Meta:
        model = Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_description', 'price', 'discount', 'image', 'is_active', 'created', 'updated']
    list_display_links = ['id', 'name']
    prepopulated_fields = {"slug": ('name',)}

    class Meta:
        model = Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
    prepopulated_fields = {"slug": ('name',)}

    class Meta:
        model = Category


class CartProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CartProduct._meta.fields]

    class Meta:
        model = CartProduct


class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cart._meta.fields]
    list_editable = ['in_order', 'for_anonymous_user']

    class Meta:
        model = Cart


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)


from django.contrib import admin
from shop.models import Order, Product, Cart, CartItem

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)

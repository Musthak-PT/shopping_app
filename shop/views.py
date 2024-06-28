from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Order
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem

class IndexView(TemplateView):
    template_name = 'shop/index.html'

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shop/product_list.html', {'products': products})

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'shop/product_detail.html', {'product': product})

class OrderListView(View):
    def get(self, request):
        orders = Order.objects.all()
        return render(request, 'shop/order_list.html', {'orders': orders})

class OrderStatusUpdateView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = request.POST.get('status')
        order.save()
        return redirect('shop:order_list')
    
#_________________________Add to cart_________________________________________

class CartDetailedView(TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = 0
        counter = 0
        cart_items = None

        try:
            cart = Cart.objects.get(user=self.request.user)
            cart_items = CartItem.objects.filter(cart=cart, active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                counter += cart_item.quantity
        except ObjectDoesNotExist:
            pass

        context['cart_items'] = cart_items
        context['total'] = total
        context['counter'] = counter
        return context

class AddToCartView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )

        return redirect('shop:cart_detail')

class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('shop:cart_detail')

class FullRemoveView(View):
    def get(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
        return redirect('shop:cart_detail')

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

#___________________________Products_Rating _____________________________
from django.contrib.auth.decorators import login_required
from shop.forms import RatingForm
from customer.models import Rating

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

class RateProductView(LoginRequiredMixin, FormView):
    form_class = RatingForm
    template_name = 'customer/product_list.html'
    
    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        rating_value = form.cleaned_data['rating']
        
        try:
            customer = self.request.user.customer
        except ObjectDoesNotExist:
            # Handle the case where the customer object does not exist
            # You can redirect to an error page or handle it appropriately
            return redirect('customer:product_list')  # or handle the error appropriately
        
        Rating.objects.update_or_create(
            customer=customer,
            product=product,
            defaults={'rating': rating_value}
        )
        return redirect('customer:product_list')
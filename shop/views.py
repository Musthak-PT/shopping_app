from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Order
from django.views.generic import TemplateView


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
def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))

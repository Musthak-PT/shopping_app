from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer, Cart, Rating
from shop.models import Product, Order
from django.db.models import Avg
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout

class CustomerSignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'customer/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            login(request, user)
            return redirect('customer:product_list')
        return render(request, 'customer/signup.html', {'form': form})

# class CustomerLoginView(View):
#     def get(self, request):
#         form = AuthenticationForm()
#         return render(request, 'customer/login.html', {'form': form})

#     def post(self, request):
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('customer:product_list')
#         return render(request, 'customer/login.html', {'form': form})
class CustomerLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'customer/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('customer:product_list')
        return render(request, 'customer/login.html', {'form': form})

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'customer/product_list.html', {'products': products})

class CartView(View):
    def get(self, request):
        cart_items = Cart.objects.filter(customer=request.user.customer)
        return render(request, 'customer/cart.html', {'cart_items': cart_items})

class AddToCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = Cart.objects.get_or_create(customer=request.user.customer, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
        return redirect('customer:cart')

class OrderListView(View):
    def get(self, request):
        orders = Order.objects.filter(customer=request.user.customer)
        return render(request, 'customer/order_list.html', {'orders': orders})

class RateProductView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        rating_value = int(request.POST.get('rating'))
        rating, created = Rating.objects.get_or_create(customer=request.user.customer, product=product)
        rating.rating = rating_value
        rating.save()

        # Update average rating
        ratings = Rating.objects.filter(product=product)
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']  # Use Avg from django.db.models
        product.average_rating = average_rating
        product.save()
        
        return redirect('customer:product_detail', pk=pk)
    
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        django_logout(request)
        return redirect('customer:login')  # Redirect to login page after logout
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
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

#______________________Customer registration view__________________________________

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
            return redirect('customer:product_list')  # Replace with your desired redirect URL
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return render(request, 'customer/signup.html', {'form': form})
    

#___________________________Customer login view_______________________________________

class CustomerLoginView(View):
    def get(self, request):
        return render(request, 'customer/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        # Check if user is authenticated and is not a superuser
        if user is not None and not user.is_superuser:
            # Log the customer in
            auth_login(request, user)
            return redirect('shop:index')  
        
        # Invalid credentials or user is a superuser
        else:
            messages.error(request, 'Invalid username or password for customer')
            return redirect('customer:customerlogin')
        

        

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
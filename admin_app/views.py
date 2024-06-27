from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from shop.models import Product
# Create your views here.

#admin home page
class AdminIndexView(TemplateView):
    template_name = 'adminindex.html'

#Admin login
class AdminLoginView(View):
    def get(self, request):
        return render(request, 'admin_login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_superuser:
            auth_login(request, user)
            return redirect('admin_app:index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('admin_app:login') 

#admin logout

class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('/')

#______________________CRUD OPERATIONS ____________________
class Productindex(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_index.html', {'products': products})
    
class Productindex(View):
    def get(self, request,product_id):
        products = Product.objects.get(id=product_id)
        return render(request, 'product_index.html', {'products': products})
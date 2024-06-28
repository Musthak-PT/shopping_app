from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from shop.models import Product
from django.shortcuts import render, get_object_or_404
from admin_app.forms import ProductForm
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
#Listing of all products
class Productindex(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_index.html', {'products': products})

#Detailed view 
class ProductDetailedView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id) 
        return render(request, 'product_details.html', {'product': product})
    
#Updating
class ProductUpdateView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(instance=product)
        return render(request, 'product_edit.html', {'form': form, 'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_app:productindex')
        return render(request, 'product_edit.html', {'form': form, 'product': product})
#Deleting
class ProductDeleteView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'product_delete.html', {'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return redirect('admin_app:productindex')
#Adding products
class ProductAddView(View):
    def get(self, request):
        return render(request, 'product_add.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        product = Product(name=name, description=description, price=price, stock=stock, image=image)
        product.save()
        return redirect('admin_app:productindex')
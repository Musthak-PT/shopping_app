from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer, Rating
from shop.models import Product, Order
from django.db.models import Avg
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from customer.serializers import CustomerRegistrationSerializer , ProductResponseSchema , OrderResponseSchema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ecommerce.response import ResponseInfo
from rest_framework import generics, filters, permissions

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
        

        
#__________________Listing of products__________________

from shop.forms import RatingForm
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        form = RatingForm()
        return render(request, 'customer/product_list.html', {'products': products, 'form': form})
    
class CustomerListView(View):
    def get(self, request):
        customer = User.objects.filter(is_superuser=False)
        return render(request, 'customer/customer_list.html', {'customer': customer})
     

    
#_________________________________Customer registration apis_____________________________


class CreateOrUpdateCustomerRegistrationApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateCustomerRegistrationApiView, self).__init__(**kwargs)
    
    serializer_class = CustomerRegistrationSerializer
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            instance = serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = "Customer successfully registered"
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = serializer.errors
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework import filters

#____________________________Listing of products____________________
class GetProductListingApiView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductResponseSchema
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        
        if instance_id:
            queryset = queryset.filter(id=instance_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
#___________________________________orders_Listing______________________

class GetOrderListingApiView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderResponseSchema
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        
        if instance_id:
            queryset = queryset.filter(id=instance_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



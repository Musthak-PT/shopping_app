from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import (
    CustomerSignupView, CustomerLoginView, ProductListView,CustomerListView, RatingListView
)

app_name = 'customer'

urlpatterns = [
    
    path('signup/', CustomerSignupView.as_view(), name='signup'),
    path('login/', CustomerLoginView.as_view(), name='customerlogin'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('customers/', CustomerListView.as_view(), name='customers_list'),
    path('rating_listing/', RatingListView.as_view(), name='rating_list'),
    
    #________________________________apis________________________________________________
    path('customer-register/', views.CreateOrUpdateCustomerRegistrationApiView.as_view()), #Customer Registration
    path('customer-login/', obtain_auth_token, name='login'), #Customer Login
    path('listing-products/', views.GetProductListingApiView.as_view()), #Listing Products
    path('listing-orders/', views.GetOrderListingApiView.as_view()), #Listing Products
    

   
]

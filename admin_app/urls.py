from django.urls import path
from .views import AdminIndexView, AdminLoginView, LogoutView, Productindex , ProductDetailedView , ProductUpdateView , ProductDeleteView ,ProductAddView

app_name = 'admin_app'

urlpatterns = [
    
    path('', AdminLoginView.as_view(), name='login'),
    path('index/', AdminIndexView.as_view(), name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),

    #CRUD Operations on the products
    path('products-index/',Productindex.as_view(),name='productindex'),
    path('productslisting/<int:product_id>',ProductDetailedView.as_view(),name='productsdetailed'),
    path('add/',ProductAddView.as_view(),name='productadd'),
    path('update/<int:product_id>/', ProductUpdateView.as_view(), name='productupdate'),
    path('delete/<int:product_id>/',ProductDeleteView.as_view(),name='productdelete')

]
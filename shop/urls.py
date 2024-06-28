from django.urls import path
from .views import ProductListView, ProductDetailView, OrderListView, OrderStatusUpdateView, IndexView, CartDetailedView, AddToCartView,CartRemoveView, FullRemoveView

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/update/', OrderStatusUpdateView.as_view(), name='order_status_update'),
    
    #Add to cart
    path('cart/', CartDetailedView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
    path('full_remove/<int:product_id>/',FullRemoveView.as_view(), name='full_remove'),

]
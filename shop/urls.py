from django.urls import path
from .views import ProductListView, ProductDetailView, OrderListView, OrderStatusUpdateView, IndexView

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/update/', OrderStatusUpdateView.as_view(), name='order_status_update'),
]
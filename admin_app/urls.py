from django.urls import path
from .views import AdminIndexView, AdminLoginView, LogoutView

app_name = 'admin_app'

urlpatterns = [
    
    path('', AdminLoginView.as_view(), name='login'),
    path('index/', AdminIndexView.as_view(), name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
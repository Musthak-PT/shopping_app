from django.urls import path
from .views import AdminIndexView, AdminLoginView, LogoutView, Productindex

app_name = 'admin_app'

urlpatterns = [
    
    path('', AdminLoginView.as_view(), name='login'),
    path('index/', AdminIndexView.as_view(), name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),

    #CRUD Operations on the products
    
    path('products-index/',Productindex.as_view(),name='productindex'),
    path('productslisting/<int:product_id>',Productindex.as_view(),name='productsdetailed'),
    
    # path('add/',views.add_movie,name='add_movie'),
    # path('update/<int:id>/',views.update,name='update'),
    # path('delete/<int:id>/',views.delete,name='delete')

]
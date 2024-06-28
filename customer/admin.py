from django.contrib import admin
from customer.models import Customer, Rating
# Register your models here.
admin.site.register(Customer)
# admin.site.register(Cart)
admin.site.register(Rating)
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name              = models.CharField(max_length=255)
    description       = models.TextField()
    price             = models.DecimalField(max_digits=10, decimal_places=2)
    stock             = models.PositiveIntegerField()
    average_rating    = models.FloatField(default=0.0)

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    customer    = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    order_date  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.user.username}"
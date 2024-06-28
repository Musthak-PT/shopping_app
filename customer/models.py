from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Customer(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.user.username

# class Cart(models.Model):
#     customer    = models.ForeignKey(User, on_delete=models.CASCADE)
#     product     = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
#     quantity    = models.PositiveIntegerField()

#     def __str__(self):
#         return f"Cart {self.id} for {self.customer.user.username}"

class Rating(models.Model):
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product     = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    rating      = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Rating {self.rating} for {self.product.name} by {self.customer.user.username}"
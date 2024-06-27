from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from random import randint


def product_image(self, filename):
    return f"shop/image/{filename}"


def product_default_image(): 
    return f"shop/image/default/default-image/default-image-for-no-image.png"

class Product(models.Model):
    slug              = models.SlugField(('Slug'), max_length=100, editable=False, null=True, blank=True)
    name              = models.CharField(max_length=255)
    description       = models.TextField()
    price             = models.DecimalField(max_digits=10, decimal_places=2)
    stock             = models.PositiveIntegerField()
    image             = models.ImageField(upload_to='gallery')
    average_rating    = models.FloatField(default=0.0)
    
    def save(self, *args, **kwargs):
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
            if Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.name)) + '-' + str(randint(1, 9999999))
        super(Product, self).save(*args, **kwargs)

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    customer    = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': False})
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    order_date  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"
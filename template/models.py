from django.db import models
from user.models import *
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group
from user .validators import phone_validator
from django.utils.timezone import now
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 

class Notification(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=True)

    def __str__(self):
        return f"Notification for {self.user_id.username} - {self.message[:50]}..."  
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_DEFAULT, default=1)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="product/", null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    description = models.TextField()
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    url = models.URLField(default=True)

    def __str__(self):
        return self.name  # Corrected typo from _str_ to __str__
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price)


class AddToCart(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_date = models.DateTimeField(default=now)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.total_price = Decimal(self.quantity) * self.product.price
        super(AddToCart, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name} - {self.product.name} ({self.quantity})"


class CartItem(models.Model):
    cart = models.ForeignKey(AddToCart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    
from django.db import models
from decimal import Decimal

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=True) 
    cart_id = models.ManyToManyField(AddToCart)  # Many-to-Many with AddToCart
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchased_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=True)
    def __str__(self):
        cart_items = self.cart_id.all()  # Get all related cart items
        item_details = ", ".join([f"{item.product.name} ({item.quantity})" for item in cart_items])
        return f"Purchase: {item_details} - Total: {self.total}"


class Billing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        related_name="billing",
        on_delete=models.CASCADE
    )
    purchases = models.ManyToManyField(Purchase, related_name="billing_purchases")
    status = models.CharField(
        max_length=100, choices=[("paid", "Paid"), ("unpaid", "Unpaid")]
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save initially to get an ID
        
        
        total_sum = self.purchases.aggregate(total_sum=Sum("total"))["total_sum"] or Decimal("0.00")

        if self.total != total_sum: 
            self.total = total_sum
            super().save(update_fields=["total"])

    def __str__(self):
        return f"Billing for {self.user.name} - Total: {self.total}"
class Review(models.Model):
    email = models.EmailField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()





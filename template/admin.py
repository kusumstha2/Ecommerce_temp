from django.contrib import admin
from .models import *

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'user', 'file', 'url')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    list_editable = ('price', 'stock')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'message', 'is_read', 'created_at')

@admin.register(AddToCart)
class AddToCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'added_date', 'total_price')
    search_fields = ('user__email',)  # Searching user by email

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")
    search_fields = ("product__name",)
    list_filter = ("cart",)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "total")  
    filter_horizontal = ("cart_id",)  

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "total")  
    list_filter = ("status",)  
    filter_horizontal = ("purchases",)  



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', "email", "comment", 'user', 'product', 'rating')
    list_filter = ("rating",)
    search_fields = ("email", "product__name")

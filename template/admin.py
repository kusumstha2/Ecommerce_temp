from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'message','is_read', 'created_at')
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")
    search_fields = ("product__name",)
    list_filter = ("cart",)
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status',)
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating')


    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    filter_horizontal = ('products',)  # This makes managing many-to-many relationships easier in admin


from django.urls import path, include
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
   
    
    path('product_category/',ProductCategoryApiView.as_view({'get':'list', 'post':'create'}), name="product_category"),
    path('product_category/<int:pk>/',ProductCategoryApiView.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="product_category_detail"),
    
    path('product/',ProductApiView.as_view({'get':'list', 'post':'create'}), name="product"),
    path('product/<int:pk>/',ProductApiView.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="product_detail"),
    
    path('purchase/',PurchaseApiView.as_view(), name="purchase"),
    path('purchase/<int:pk>/',PurchaseDetailApiView.as_view(), name="purchase_detail"),
    
    path('billing/',BillingApiView.as_view({'get':'list', 'post':'create'}), name="billing"),
    path('billing/<int:pk>/',BillingApiView.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="billing_detail"),
    
    path('addtocart/',AddToCartViewSet.as_view({'get':'list', 'post':'create'}), name="addtocart"),
    path('addtocart/<int:pk>/',AddToCartViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="addtocart_detail"),
    
    path('cartitem/',CartItemViewSet.as_view({'get':'list', 'post':'create'}), name="cartitem"),
    path('cartitem/<int:pk>/',CartItemViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="cartitem_detail"),
    
    path('review/',ReviewViewSet.as_view({'get':'list', 'post':'create'}), name="review"),
    path('review/<int:pk>/',AddToCartViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="review_detail"),
    

    path('notification/',NotificationViewSet.as_view({'get':'list', 'post':'create'}), name="notification"),
    path('notification/<int:pk>/',NotificationViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}), name="notification_detail"),
]
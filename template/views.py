from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from user .validators import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from .permissions import *

# Notifications ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

class ProductApiView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['category']
    search_fields = ['name','description']
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        category = request.data.get('category')
        price = request.data.get('price')
        stock = request.data.get('stock')

        if not (name and category and price and stock):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to find existing product with same name, category, price
            existing_product = Product.objects.get(name=name, category=category, price=price)
            existing_product.stock += int(stock)
            existing_product.save()
            serializer = self.get_serializer(existing_product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            # Create new product if not found
            return super().create(request, *args, **kwargs)
    
class PurchaseDetailApiView(GenericAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            queryset = Purchase.objects.get(id=pk)
        except:
            return Response("Purchase Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            queryset = Purchase.objects.get(id=pk)
        except:
            return Response("Purchase Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Data Updated!")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            queryset = Purchase.objects.get(id=pk)
        except:
            return Response("Purchase Not Found", status=status.HTTP_404_NOT_FOUND)
        queryset.delete()
        return Response("Data Deleted!")

    def patch(self, request, pk=None):
        queryset = self.get_object()
        serializer = PurchaseSerializer(instance=queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AddToCart
from .serializers import AddToCartSerializer

class AddToCartViewSet(viewsets.ModelViewSet):
    queryset = AddToCart.objects.all()
    serializer_class = AddToCartSerializer

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        user = request.user

        # Check if user is authenticated
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=400)

        product_id = request.data.get('product')
        quantity = request.data.get('quantity')

        # Validate required fields
        if not product_id or not quantity:
            return Response({"error": "Product and quantity are required."}, status=400)

        try:
            # Ensure product exists
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        # Ensure quantity is a positive integer
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than zero."}, status=400)
        except ValueError:
            return Response({"error": "Quantity must be a valid integer."}, status=400)

        # Create AddToCart instance
        add_to_cart_instance = AddToCart.objects.create(
            user=user,
            product=product,
            quantity=quantity,
        )

        # Serialize the created AddToCart instance and return response
        serializer = AddToCartSerializer(add_to_cart_instance)
        return Response(serializer.data, status=201)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    

# Category ViewSet
class ProductCategoryApiView(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filterset_fields = ['name']
    search_fields = ['name']
    
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Billing
from .serializers import BillingSerializer
class BillingApiView(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        
        # Access cart items through the related name defined in AddToCart model
        cart_items = AddToCart.objects.filter(user=user)  # No need to modify AddToCart model

        if not cart_items:
            return Response({"error": "No items in cart."}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.total_price for item in cart_items)
        
        # Here we use 'total' instead of 'total_amount'
        billing_instance = Billing.objects.create(
            user=user,
            total=total_amount,  # Use total instead of total_amount
            status='Pending'  # Or any default status
        )

        # You can add more logic to handle the payment and other fields
        serializer = self.get_serializer(billing_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class PurchaseApiView(GenericAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_ids = request.data.get('cart_id', [])  # Get list of cart IDs

        if not isinstance(cart_ids, list):  # Validate list
            return Response({"cart_id": ["Expected a list of cart item IDs."]}, status=status.HTTP_400_BAD_REQUEST)

        purchase = Purchase.objects.create(total=0)  # Create Purchase instance
        total_amount = Decimal(0)

        for cart_id in cart_ids:
            cart_item = get_object_or_404(AddToCart, id=cart_id)
            product = cart_item.product
            quantity = cart_item.quantity

            if product.stock >= quantity:
                product.stock -= quantity  # Reduce stock
                product.save()
                purchase.cart_id.add(cart_item)  # Link cart item to purchase
                total_amount += product.price * quantity  # Calculate total
            else:
                return Response({"error": f"Stock is too low for {product.name}."}, status=status.HTTP_400_BAD_REQUEST)

        purchase.total = total_amount
        purchase.save()

        return Response(PurchaseSerializer(purchase).data, status=status.HTTP_201_CREATED)

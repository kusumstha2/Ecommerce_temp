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
    
class AddToCartViewSet(viewsets.ModelViewSet):
    queryset = AddToCart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddToCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        
        # Check if the product already exists in the user's cart
        cart_item = AddToCart.objects.filter(user=user, product=product).first()
        
        if cart_item:
            # If the product is already in the cart, update the quantity
            cart_item.quantity += quantity
            cart_item.total_price = cart_item.quantity * cart_item.product.price  # Recalculate the total price
            cart_item.save()  # Save the updated cart item
        else:
            
            serializer.save(user=user)


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
    search_fields = ['user__username', 'status']


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

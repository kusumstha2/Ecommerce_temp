from rest_framework import serializers
from .models import *

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.name if instance.category else None
        
        return representation

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"





class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"
class ReviewSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.user  # Get the user instance

        representation['product_name'] = instance.product.name if instance.product else None
        representation['user_email'] = user.email if user and user.email else None  

        return representation

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating should be between 1 and 5.")
        return value

    class Meta:
        model = Review
        fields = '__all__'





from rest_framework import serializers
from decimal import Decimal

class PurchaseSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cart_items = instance.cart_id.all()  # Get all cart items

        total_price = Decimal(0)  # Initialize total
        products_list = []  # Store product names

        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            price = product.price
            total_price += price * quantity
            products_list.append(f"{product.name} (x{quantity})")

        representation['total'] = str(total_price)  # Store total
        representation['products'] = products_list  # Store product details

        return representation

from rest_framework import serializers
from decimal import Decimal

class BillingSerializer(serializers.ModelSerializer):
    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Billing
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        purchases_data = []
        total = Decimal(0)

        if instance.user: 
            for purchase in instance.purchases.all():  
               
                purchased_date_local = purchase.purchased_date or None
                if purchased_date_local:
                    purchased_date_time = purchased_date_local.isoformat()
                else:
                    purchased_date_time = None  

                purchase_data = {
                    'product': purchase.product.name if purchase.product else None,
                    'price': format(purchase.product.price, '.2f') if purchase.product and purchase.product.price else None,
                    'quantity': purchase.quantity if hasattr(purchase, 'quantity') else None,
                    'total': format(purchase.total, '.2f') if purchase.total else None,
                    'purchased_date_time': purchased_date_time,
                }
                purchases_data.append(purchase_data)
                total += Decimal(purchase.total) if purchase.total else Decimal(0)

        representation['user'] = instance.user.username if instance.user else None  
        representation['total'] = format(total, '.2f')
        representation['purchases'] = purchases_data
        return representation

    def create(self, validated_data):
        user = validated_data.get('user')  
        billing = Billing.objects.create(user=user, status=validated_data.get('status'))

     
        purchases = Purchase.objects.filter(cart_id__in=user.cart_items.all())  

        billing.purchases.set(purchases)

        
        total = purchases.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        billing.total = total
        billing.save()
        return billing
    
from rest_framework import serializers
from .models import AddToCart  # Import your model
from decimal import Decimal

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCart
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'added_date']
from daraz.models import  User, Customer, Product, Cart, Orderplaced
from rest_framework import serializers  
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['email', 'name', 'is_active', 'is_staff', 'is_seller', 'is_customer', 'is_superuser', 'created_at', 'updated_at']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'name', 'province', 'city', 'address', 'landmark', 'phone_number', 'gender']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'color', 'product_image']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']

class OrderplacedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderplaced
        fields = ['user', 'customer', 'product', 'quantity', 'ordered_date', 'status']
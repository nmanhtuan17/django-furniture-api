from rest_framework import serializers 
from app.models import Product, User, Cart, Category, Order

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = '__all__'
    
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      'email',
      'username',
      'password',
    )
    
class CardSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cart
    fields = '__all__'
    
class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = '__all__'
    

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'
      
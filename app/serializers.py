from rest_framework import serializers 
from app.models import Product, User

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ('id',
              'name',
              'photo',
              'price',
              'description',
              'stock_quantity')
    
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      'email',
      'username',
      'password',
    )
      
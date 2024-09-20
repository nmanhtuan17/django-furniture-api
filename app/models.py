from django.db import models
from django.core.validators import MinLengthValidator

class Product(models.Model):
  name = models.TextField()
  category = models.TextField(blank=False)
  photo = models.TextField(blank=True)
  price = models.PositiveIntegerField()
  description = models.TextField(blank=True)
  stock_quantity = models.SmallIntegerField(blank=False)

class User(models.Model):
  email = models.EmailField()
  username = models.TextField(blank=True)
  password = models.TextField(validators=[
              MinLengthValidator(6, 'the field must contain at least 6 characters')
            ])
  isAdmin = models.BooleanField()
  
  
class Cart(models.Model):
  product = models.TextField()
  user = models.TextField()
  quantity = models.SmallIntegerField()
  

class Order(models.Model):
  products = models.JSONField()
  user = models.TextField(blank=True)
  username = models.TextField()
  status = models.TextField(blank=True)
  payment = models.BooleanField(blank=True)
  address = models.TextField()
  total = models.PositiveIntegerField()
  phone = models.PositiveIntegerField()
  
class Category(models.Model):
  name = models.TextField()
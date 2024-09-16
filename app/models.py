from django.db import models
from django.core.validators import MinLengthValidator

class Product(models.Model):
  name = models.TextField()
  photo = models.TextField(blank=False)
  price = models.PositiveIntegerField()
  description = models.TextField(blank=False)
  stock_quantity = models.SmallIntegerField(blank=False)

class User(models.Model):
  email = models.EmailField()
  username = models.TextField(blank=True)
  password = models.TextField(validators=[
              MinLengthValidator(6, 'the field must contain at least 6 characters')
            ])
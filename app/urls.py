from django.urls import path

from . import views

urlpatterns = [
  path('auth/sign-in', views.login),
  path('auth/register', views.register),
  path('products', views.product_list),
  path('products/<str:id>', views.product_detail),
  path('photo', views.upload_photo),
  path('cart/<str:id>', views.cart),
  path('category', views.category),
  path('category/<str:id>', views.category_detail),
  path('order', views.get_all_order),
  path('order/<str:id>', views.order),
  
]
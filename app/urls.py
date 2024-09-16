from django.urls import path

from . import views

urlpatterns = [
  path('auth/sign-in', views.login),
  path('auth/register', views.register),
  path('products', views.product_list),
  path('photo', views.upload_photo)
  ]
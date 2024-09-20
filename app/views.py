from django.http import HttpResponse
from pymongo import MongoClient, ReturnDocument
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import status
 
from app.models import Product
from app.serializers import ProductSerializer, UserSerializer, CardSerializer, CategorySerializer, OrderSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from app.utils import serialize_mongo_document, hash_password, check_password, upload_image
from bson import ObjectId
from . import type

client = MongoClient('mongodb+srv://tuanmnguye:Ob47mBLkGbWhXuUL@django.oi103.mongodb.net/?retryWrites=true&w=majority&appName=django')
dbname = client['django']
user_collection = dbname['user']
product_collection = dbname['product']
cart_collection = dbname['cart']
category_collection = dbname['category']
order_collection = dbname['order']


@api_view(['POST'])
def login(request):
  user = JSONParser().parse(request)
  user_serializer = UserSerializer(data=user)
  print(user)
  if user_serializer.is_valid():
    account = user_collection.find_one({'email': user_serializer.data['email']})
    if account:
      if check_password(user_serializer.data['password'], account['password']):
        print(account)
        serialize = serialize_mongo_document(account)
        serialize.pop('password')
        return JsonResponse(serialize, status=status.HTTP_200_OK, safe=False)
      else:
        return JsonResponse({'error': 'Password wrong'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
    else:
      return JsonResponse({'error': 'Account not found!'}, status=status.HTTP_400_BAD_REQUEST, safe=False)
  return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
  user = JSONParser().parse(request)
  user_serializer = UserSerializer(data=user)

  if user_serializer.is_valid():
    print(user_serializer.data['username'])
    checkUser = list(user_collection.find({'email': user_serializer.data['email']}))
    if checkUser:
      return JsonResponse({'error': 'Account already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
      hashPassword = hash_password(user_serializer.data['password'])
      print(hashPassword)
      user_collection.insert_one({'email': user_serializer.data['email'],
                                  'username': user_serializer.data['username'],
                                  'password': hashPassword})
    return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
  return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
@api_view(['GET', 'POST', 'DELETE'])
def product_list(request):
  if request.method == 'GET':
    data = list(product_collection.find({}))
    serialized_documents = [serialize_mongo_document(doc) for doc in data]
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False) 
  elif request.method == 'POST':
    product_data = JSONParser().parse(request)
    product_serializer = ProductSerializer(data=product_data)
    if product_serializer.is_valid():
      product_collection.insert_one(product_serializer.data)
      return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
@api_view(['GET', 'POST', "DELETE"])
def product_detail(request, id):
  if request.method == 'GET':
    try:
      product = product_collection.find_one({'_id': ObjectId(id)})
      serialize = serialize_mongo_document(product)
      return JsonResponse(serialize, status=status.HTTP_200_OK, safe=False)
    except Exception as error:
      return JsonResponse({'message': 'not found product'}, status=status.HTTP_404_NOT_FOUND)
  elif request.method == 'POST':
    product_data = JSONParser().parse(request)
    product_serialize = ProductSerializer(product_data)
    try:
      update_product = product_collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': product_serialize.data}, return_document=ReturnDocument.AFTER)
      return JsonResponse(serialize_mongo_document(update_product), status=status.HTTP_200_OK)
    except Exception as error:
      print(error)
      return JsonResponse({'message': 'Update product fail'}, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    try:
      product_collection.find_one_and_delete({'_id': ObjectId(id)})
      return JsonResponse({'messge': 'Success'}, status=status.HTTP_200_OK)
    except Exception as error:
      print(error)
      return JsonResponse({'message': 'Delete product fail'}, status=status.HTTP_400_BAD_REQUEST) 
    
    
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_photo(request):
  try:
    if 'photo' in request.FILES:
      file = request.FILES['photo']
      res = upload_image(file)
      print(res)
      return JsonResponse({'url': res['url']}, status=status.HTTP_201_CREATED) 
  except Exception as error:
    return JsonResponse({'error': 'upload failed'}, status=status.HTTP_400_BAD_REQUEST) 
  


## CART
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def cart(request, id):
  if request.method == 'GET':
    data = list(cart_collection.find({'user': id}))
    serialized_documents = [serialize_mongo_document(doc) for doc in data]
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    cart_serializer = CardSerializer(data=data)
    if cart_serializer.is_valid():
      check = cart_collection.find_one({'product': cart_serializer.data['product'], 'user': id})
      if check:
        print('check', check)
        updateCart = cart_collection.find_one_and_update({'_id': check['_id']}, {'$set': { 'quantity': check['quantity'] + cart_serializer.data['quantity'] }}, return_document=ReturnDocument.AFTER)
        return JsonResponse(serialize_mongo_document(updateCart), status=status.HTTP_200_OK)
      cart_collection.insert_one(cart_serializer.data)
      return JsonResponse(cart_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'PUT':
    data = JSONParser().parse(request)
    cart_serializer = CardSerializer(data=data)
    cartId = request.query_params.get('cartId')
    
    try:
      if cart_serializer.is_valid():
        updated = cart_collection.find_one_and_update({'_id': ObjectId(cartId)}, {'$set': cart_serializer.data}, return_document=ReturnDocument.AFTER)
        return JsonResponse(serialize_mongo_document(updated), status=status.HTTP_200_OK)
    except Exception as error:
      print(error)
      return JsonResponse({'message': error}, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    try:
      cartId = request.query_params.get('cartId')
      cart_collection.find_one_and_delete({'_id': ObjectId(cartId)})
      return JsonResponse({'messge': 'Success'}, status=status.HTTP_200_OK)
    except Exception as error:
      print(error)
      return JsonResponse({'message': 'Delete cart fail'}, status=status.HTTP_400_BAD_REQUEST) 

## ORDER
@api_view(['GET', 'PUT'])
def get_all_order(request):
  if request.method == 'GET':
    orders = list(order_collection.find({}))
    serialized_documents = [serialize_mongo_document(doc) for doc in orders]
    return JsonResponse(orders, status=status.HTTP_200_OK, safe=False)
  elif request.method == 'PUT':
    try:
      payload = JSONParser().parse(request)
      print(payload)
      orderId = request.query_params.get('orderId')
      print(orderId)
      updated = order_collection.find_one_and_update({'_id': ObjectId(orderId)}, {'$set': payload}, return_document=ReturnDocument.AFTER)
      return JsonResponse(serialize_mongo_document(updated), status=status.HTTP_200_OK, safe=False)
    except Exception as error:
      pass
    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def order(request, id):
  if request.method == 'GET':
    orders = list(order_collection.find({'user': id}))
    serialized_documents = [serialize_mongo_document(doc) for doc in orders]
    return JsonResponse(orders, status=status.HTTP_200_OK, safe=False)
  elif request.method == 'POST':
    payload = JSONParser().parse(request)
    serialize = OrderSerializer(data=payload)
    if serialize.is_valid():
      print(serialize.data)
      order_collection.insert_one({
        **serialize.data,
        'user': id,
        'status': type.PENDING,
        'payment': True,
      })
      cart_collection.delete_many({'user': id})
      return JsonResponse(serialize.data, status=status.HTTP_201_CREATED, safe=False)
    return JsonResponse(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    orderId = request.query_params.get('orderId')
    order_collection.find_one_and_delete({'_id': ObjectId(orderId)})
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
      

## CATEGORY
@api_view(['GET', 'POST'])
def category(request):
  if request.method == 'GET':
    data = list(category_collection.find({}))
    serialized_documents = [serialize_mongo_document(doc) for doc in data]
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    category_serializer = CategorySerializer(data=data)
    if category_serializer.is_valid():
      category_collection.insert_one(category_serializer.data)
      return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['DELETE'])
def category_detail(request, id):
  try:
    category_collection.find_one_and_delete({'_id': ObjectId(id)})
    return JsonResponse({'messge': 'Success'}, status=status.HTTP_200_OK)
  except Exception as error:
    print(error)
    return JsonResponse({'message': 'Delete category fail'}, status=status.HTTP_400_BAD_REQUEST) 


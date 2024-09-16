from django.http import HttpResponse
from pymongo import MongoClient
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import status
 
from app.models import Product
from app.serializers import ProductSerializer, UserSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from app.utils import serialize_mongo_document, hash_password, check_password, upload_image

client = MongoClient('mongodb+srv://tuanmnguye:Ob47mBLkGbWhXuUL@django.oi103.mongodb.net/?retryWrites=true&w=majority&appName=django')
dbname = client['django']
user_collection = dbname['user']
product_collection = dbname['product']

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
    print(data)
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False) 
  elif request.method == 'POST':
    product_data = JSONParser().parse(request)
    product_serializer = ProductSerializer(data=product_data)
    if product_serializer.is_valid():
      print(product_serializer)
      product_collection.insert_one(product_serializer.data)
      return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    print('')
      
@api_view(['GET', 'POST'])
def product_detail(request):
  if True:
    print('')
    
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
  
    

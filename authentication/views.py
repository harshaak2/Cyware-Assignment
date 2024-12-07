import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# @csrf_exempt
# def login(request):
#   if request.method == "POST":
#     try:
#       data = json.loads(request.body)
#       username = data.get("username")
#       password = data.get("password")

#       # if not User.objects.filter(username=username).exists():
#       #   return JsonResponse({"error": "No username found"})
    
#       user = authenticate(username=username, password=password)

#       if user:
#         auth_login(request, user)
#         return JsonResponse({"message": "Login Successful"})
#       else:
#         return JsonResponse({"error": "Invalid Credentials"})
      
#     except json.JSONDecodeError:
#       return JsonResponse({"error": "Invalid JSON"}, status=400)
    
#   return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def register(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      username = data.get("username")
      password = data.get("password")
      email = data.get("email")

      if not email:
        return JsonResponse({"error": "Email is missing"}, status=400)

      if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "username already exists"})
      
      user = User.objects.create_user(username=username, password=password, email=email)
      return JsonResponse({"message": "user created"}, status=201)
    
    except json.JSONDecodeError:
      return JsonResponse({"error": "Invalid JSON"}, status=400)
  
  return JsonResponse({"error": "Method not allowed"}, status=405)
  

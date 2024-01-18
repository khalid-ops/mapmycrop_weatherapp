from django.shortcuts import render
from django.db import models
from . models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weather_project.settings import SECRET_KEY, ACCESS_TOKEN_LIFETIME, ALGORITHM
import re
import bcrypt
import traceback
import base64
import jwt
import requests 
import json
from datetime import datetime
from .decorators import authorizer
# Create your views here.

@api_view(['POST'])
def register_user(request):

    try:
        user_data = request.data
        if User.objects.filter(user_name=user_data['name']).exists():
            return Response({'message' : 'User already exists!'}, 400)
        else:
            if len(user_data['name']) > 500:
                return Response({'message' : 'Invalid name, Nos of characters allowed for username is 500!'}, 400)
            if len(user_data['password']) > 128:
                return Response({'message' : 'Invalid password, Nos of characters allowed for password is 128!'}, 400)
            if user_data['name'] is not None:
                if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', user_data['password']):
                    hashed_pass = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
                    user = User.objects.create(
                        user_name = user_data['name'],
                        password = hashed_pass
                    )
                    if user.id:
                        return Response({'message': "User registered successfully", 'userId' : user.id}, 201)
                else:
                    return Response({'message': 'password length should be 8 or more'}, 400)
    except Exception as err:
        traceback.print_exc()
        return Response({"error": str(err)}, status=400)
    
# print(bcrypt.checkpw("khalid@123".encode('utf-8'), b'$2b$12$SiA.kce91L1PUq1guPYfm.WNld5zWcXtBgeKrogItE/dO68xssqwa'))

@api_view(['POST'])
def user_authenticate(request):

    try:
        data = request.data
        name = data["username"]
        password = data["password"]

        if User.objects.filter(user_name = name).exists():

            user = User.objects.get(user_name = name)
            pass_ = user.password
            check = bcrypt.checkpw(str(password).encode('utf-8'), pass_)
            if user.user_name == name and check:

                access_token = jwt.encode(
                    {
                    "user_id": user.id,
                    "exp": datetime.utcnow() + ACCESS_TOKEN_LIFETIME,  
                    },
                    SECRET_KEY,
                    ALGORITHM
                )

                response_payload = {
                    "message" : 'User authenticated',
                    "token": access_token,
                    "user_id": user.id,
                }

                return Response(response_payload,200)
            else:
                return Response({'message' : "Invalid user details"}, 401)
        else:
            return Response({'message' : "User not found"}, 404)

    except Exception as err:
        traceback.print_exc()
        return Response({"error": str(err)}, status=400)
    

@api_view(['GET'])
@authorizer
def authorized_endpoint(request):

    try: 
        response_payload = {
            "message" : "Api authorized with token successfully!"
        }
        return Response(response_payload, 200)
    except Exception as err:
        traceback.print_exc()
        return Response({"error": str(err)}, status=400)
    

@api_view(['GET'])
def get_api_data(request):

    try:
        req_data = request.query_params
        if len(req_data) == 0:
            return Response({"message" : "No parameters recieved"}, 400)
        if not req_data['longitude']:
            return Response({"message" : "longitude required"}, 400)
        if not req_data['latitude']:
            return Response({"message" : "latitude required"}, 400)
        if not req_data['days']:
            return Response({"message" : "days required"}, 400)
    

        response_data = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": float(req_data['latitude']),
            "longitude" : float(req_data['longitude']),
            "past_days" : int(req_data['days']),
            "hourly": ['temperature_2m', 'precipitation', 'cloud_cover'],
        }, verify=False)

        data = response_data.json()

        send_data = {
            "hourlyTemperature": data['hourly']['temperature_2m'],
            "precipitation": data['hourly']['precipitation'],
            "cloudCover" : data['hourly']['cloud_cover']
        }

        return Response(send_data, 200)
    except Exception as err:
        traceback.print_exc()
        return Response({"error": str(err)}, status=400)

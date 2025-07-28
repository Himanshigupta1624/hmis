from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import UserRegisterSerializer,UserProfileSerializer,UserLoginSerializer
from .models import CustomUser

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer=UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'user':UserProfileSerializer(user).data,
            'token':token.key,
            'message':'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer=UserProfileSerializer(data=request.data)  
    if serializer.is_valid():
        user=serializer.validated_data['user']
        login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        })
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET','PUT'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    if request.method=='GET':
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data)  
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({'message':'Logout successful'})  
    except:
        return Response({'message':'Logout successful'})  

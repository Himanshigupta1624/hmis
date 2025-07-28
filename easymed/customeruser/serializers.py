from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    password_confirm=serializers.CharField(write_only=True)
    
    class Meta:
        model=CustomUser
        fields=['email','username','first_name','last_name','phone','role','password','password_confirm']
    def validate(self, attrs):
        if attrs['password']!=attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user=CustomUser.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        if email and password:
            user=authenticate(username=email,password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')    
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user']=user
        else:
            raise serializers.ValidationError('Must include email and password')    
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id', 'email', 'username', 'first_name', 'last_name', 'phone', 'address', 
                 'date_of_birth', 'profile_picture', 'role', 'created_at'] 
        read_only_fields = ['id', 'email', 'created_at']   
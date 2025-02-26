from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=['id','email','first_name','last_name','username','phone_no','address','avatar','role','date_joined']
        read_only_fields=['id','email','role','date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=6)
    class Meta:
        model=UserProfile
        fields=['username','first_name','last_name','email','password','role','nationality']
     
    def create(self,validated_data):
        user=UserProfile.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
            email=validated_data['email'],
            role=validated_data.get('role','buyer'),
            nationality=validated_data.get('nationality',''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=('address','phone_no','avatar',)

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True,min_length=6)
    
    def validate(self,data):
        user=authenticate(email=data['email'],password=data['password'])
        if user and user.is_active:
            return user
        return serializers.ValidationError('Invalid login credidentials')

class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField()
    
    def validate_email(self,data):
        if not UserProfile.objects.filter(email=data).exists():
            raise serializers.ValidationError('Email does not exist')
        return data
   


        

        
   


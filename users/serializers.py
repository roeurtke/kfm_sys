from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Add CustomTokenObtainPairSerializer for login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Invalid email or password. Please try again.'
    }
    
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data['message'] = "Login successfully"
            data['username'] = self.user.username
            data['email'] = self.user.email
            return data
        except Exception as e:
            raise serializers.ValidationError({"message": "Invalid credentials. Please check your email and password."})

class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    default_error_messages = {
        'invalid_token': 'Invalid token. Please provide a valid refresh token.'
    }

    def validate(self, attrs):
        try:
            super().validate(attrs)
            return {"message": "Logout successfully"}
        except Exception as e:
            raise serializers.ValidationError({"message": "Invalid token. Please check your refresh token."})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)  # Prevent ID from being modified        
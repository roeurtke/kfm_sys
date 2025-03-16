from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from roles.models import Role
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
    role = serializers.SlugRelatedField(
        queryset=Role.objects.all(),  # Fetch all roles from the database
        slug_field='name',  # Use the 'name' field of the Role model
        allow_null=True,  # Allow the role to be null
        required=False  # The role field is optional
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = ('id',)  # Prevent ID from being modified
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make username and email optional during updates
        if self.context.get('request').method in ['PUT', 'PATCH']:
            self.fields['username'].required = False
            self.fields['email'].required = False

    def create(self, validated_data):
        role_data = validated_data.pop('role', None)  # Extract the role data
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data.get('password', '')  # Password is optional here
        )
        
        # Assign the role if provided
        if role_data:
            user.role = role_data
            user.save()
        
        return user

    def update(self, instance, validated_data):
        # Update the user instance with the validated data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        # Update the role if provided
        if 'role' in validated_data:
            instance.role = validated_data['role']
        
        # Update the password if provided
        if 'password' in validated_data:
            instance.password(validated_data['password'])
            
        instance.save()
        return instance
    
    def to_representation(self, instance):
        # Customize the response for both create and update operations
        if self.context.get('is_update', False):
            message = "User updated successfully"
        else:
            message = "User created successfully"

        return {
            "message": message,
            "user": {
                "id": instance.id,
                "username": instance.username,
                "email": instance.email,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "role": instance.role.name if instance.role else None,
                "password": instance.password
            }
        }
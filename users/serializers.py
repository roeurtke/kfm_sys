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
            data['username'] = self.user.username
            data['message'] = "Login successfully"
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
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'password')
        read_only_fields = ('id',)
        
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
            password=validated_data['password']
        )

        # Assign the default role if no role is provided
        if not role_data:
            default_role = Role.objects.get(name="Normal")
            user.role = default_role
        else:
            user.role = role_data
        
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        if 'role' in validated_data:
            instance.role = validated_data['role']
    
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            
        instance.save()
        return instance
    
    def to_representation(self, instance):
        # Customize the response for both create and update operations
        if self.context.get('is_update', False):
            message = "User updated successfully"
        elif self.context.get('is_create', False):
            message = "User created successfully"
        else:
            message = None

        response_data = {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "role": instance.role.name if instance.role else None
        }

        if message:
            return {
                "message": message,
                "user": response_data
            }
        return response_data
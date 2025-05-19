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
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Password fields didn't match."})
        
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"error": "Email already exists."})
        
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        default_role = Role.objects.get(name="Normal")
        user.role = default_role
        user.save()

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
            return data
        except Exception as e:
            raise serializers.ValidationError({"error": "Invalid credentials. Please check your email and password."})

class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    default_error_messages = {
        'invalid_token': 'Invalid token. Please provide a valid refresh token.'
    }

    def validate(self, attrs):
        try:
            super().validate(attrs)
            return {"message": "Logout successfully"}
        except Exception as e:
            raise serializers.ValidationError({"error": "Invalid token. Please check your refresh token."})

class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'password',
            'spending_limit',
            'status',
            'deleted_at',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
        
    # Make username and email optional during updates
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request').method in ['PUT', 'PATCH']:
            for field in ['username', 'first_name', 'last_name', 'email', 'spending_limit', 'role', 'password']:
                self.fields[field].required = False

    #Ensure spending_limit is non-negative.
    def validate_spending_limit(self, value):
        if value < 0:
            raise serializers.ValidationError({"error": "Spending limit cannot be negative."})
        return value
    
    def create(self, validated_data):
        # Extract role and spending_limit from validated_data
        role = validated_data.pop('role', None)
        spending_limit = validated_data.pop('spending_limit', 0.00)

        # Create the user with the remaining validated data
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            spending_limit=spending_limit
        )

        # Assign the role if provided and validate its existence
        if role:
            if not Role.objects.filter(id=role.id).exists():
                raise serializers.ValidationError({"role": "Invalid role provided."})
            user.role = role
            user.save()  # Save the user again to update the role

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.spending_limit = validated_data.get('spending_limit', instance.spending_limit)
        
        # Update role if provided
        if 'role' in validated_data:
            role = validated_data['role']
            if not Role.objects.filter(id=role.id).exists():
                raise serializers.ValidationError({"error": "Invalid role provided."})
            instance.role = role
        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        if 'status' in validated_data:
            instance.status = validated_data['status']
            if validated_data['status']:
                instance.is_active = True
            else:
                instance.is_active = False
            
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "spending_limit": instance.spending_limit,
            "role": {
                "name": instance.role.name
            } if instance.role else None,
            "status": instance.status,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }
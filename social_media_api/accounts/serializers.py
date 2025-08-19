# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details (excluding password)
    """
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count']
        read_only_fields = ['id', 'followers_count', 'following_count']
        

# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token  # Add this import

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details (excluding password)
    """
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = User  # Use get_user_model() result
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count']
        read_only_fields = ['id']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User  # Use get_user_model() result
        fields = ['username', 'email', 'bio', 'password', 'password_confirm']
    
    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirm from validated_data
        validated_data.pop('password_confirm')
        
        # Create user with hashed password
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)  # Use get_user_model()
        user.set_password(password)
        user.save()
        
        # Create token for the new user
        Token.objects.create(user=user)  # Add this line
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        attrs['user'] = user
        return attrs
    


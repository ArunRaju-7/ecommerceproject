
from rest_framework import serializers
from .models import User
import jwt
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'token']

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)
        if not email or not password:
            raise serializers.ValidationError("Email and password are required for login.")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password.')
        token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")

        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token
        }
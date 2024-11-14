from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializer, UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib import auth


# Create your views here.

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('email', None)
        password = data.get('password', None)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            return Response({"data": "Already Logged in"}, status=status.HTTP_200_OK)

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                print(serializer.validated_data)
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"data": "Logged Out"}, status=status.HTTP_200_OK)
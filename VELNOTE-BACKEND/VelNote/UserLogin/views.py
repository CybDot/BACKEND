from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer , UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication , SessionAuthentication , BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()  # Create user
                refresh = RefreshToken.for_user(user)  # Generate tokens
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "email": user.email,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    "message": "Registration successful!"
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            # Extract email and password from the validated data
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate using email and password
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "is_verified": user.is_verified,
                    },
                    "message": "Login successful!"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
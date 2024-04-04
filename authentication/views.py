from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from authentication.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthUserAPIView(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = JWTAuthentication().get_validated_token(refresh)
            
            # Return response with both tokens and user data
            return Response({
                "access_token": str(access_token),
                "refresh_token": str(refresh),
                "user": LoginSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication


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

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(username=email, password=password)
            if user:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from authentication.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers


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
            token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            # Include user data and token in the response
            serializer = LoginSerializer(user)  # Use LoginSerializer instead of RegisterSerializer
            data = serializer.data
            data['token'] = token  # Include the token data

            return JsonResponse(
                {"status": "success", "data": data},
                status=status.HTTP_200_OK,
                safe=False,
            )
        else:
            return Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)



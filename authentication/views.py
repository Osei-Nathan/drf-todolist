from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from authentication.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class AuthUserAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = LoginSerializer

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)
        serializer = self.serializer_class(user)
        response_data = serializer.data

        refresh = RefreshToken.for_user(user)
        token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        
        response_data['token'] = token

        return Response(response_data,status=status.HTTP_200_OK)
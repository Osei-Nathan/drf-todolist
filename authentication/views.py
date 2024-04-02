from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from django.contrib.auth import authenticate

class AuthUserAPIView(GenericAPIView):
    authentication_classes = [authentication.SessionAuthentication]  # Use appropriate authentication class
    serializer_class = RegisterSerializer

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response({'user': serializer.data})

class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)



# Create your views here.

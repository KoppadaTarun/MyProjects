from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializer import RegistrationSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['message'] = "Registration Successful"
            data['email'] = user.email
            data['username'] = user.username
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        User = authenticate(username= email, password= password)
        data = {}
        if User:
            refresh = RefreshToken.for_user(User)
            data['token'] = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['error'] = "Invalid Username or Password!"
            return Response(data, status= status.HTTP_400_BAD_REQUEST )

@api_view(['POST'])
def logout_view(request):

    try:
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



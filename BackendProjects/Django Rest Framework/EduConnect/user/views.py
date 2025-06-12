from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, AuthTokenSerialzer
from rest_framework.settings import api_settings

class RegisterStudentView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        serializer.save(is_student=True, is_instructor=False)


class RegisterInstructorView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        serializer.save(is_student=False, is_instructor=True)

class AuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerialzer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



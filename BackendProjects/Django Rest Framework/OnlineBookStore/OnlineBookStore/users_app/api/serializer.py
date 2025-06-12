from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    ConfirmPassword = serializers.CharField(style='password', write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'ConfirmPassword', 'username']
        extra_kwargs = {
            "password": {
                'write_only':True
            }
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['ConfirmPassword']

        User = get_user_model()

        if User.objects.filter(email= self.validated_data['email']).exists():
            raise serializers.ValidationError("Email already Exists")

        if password != password2:
            raise serializers.ValidationError("password and password2 must be same!")

        user = User.objects.create(email = self.validated_data['email'], username = self.validated_data['username'])
        user.set_password(password)
        user.save()
        return user

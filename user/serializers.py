from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from .models import Author, Translator

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone_num', 'birth_date', 'gender', 'password']

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise AuthenticationFailed(_('Invalid credentials or inactive user.'))

            if not user.is_active:
                raise AuthenticationFailed(_('User account is disabled.'))

        else:
            raise AuthenticationFailed(_('Must include "email" and "password".'))

        attrs['user'] = user
        return attrs

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'author', 'bio']

class TranslatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translator
        fields = ['id', 'author', 'bio']



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.name
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active

        return token


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = RefreshToken(attrs['refresh'])

        user_id = refresh['user_id']

        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.filter(id=user_id).first()

        if user is not None:
            access_token = refresh.access_token
            access_token['username'] = user.name
            access_token['email'] = user.email
            access_token['is_staff'] = user.is_staff
            access_token['is_active'] = user.is_active

            data['access'] = str(access_token)

        return data
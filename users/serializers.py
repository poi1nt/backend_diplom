from django.contrib.auth.hashers import make_password
from pyexpat.errors import messages
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

from files.models import File
from users.models import User


class UserFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['size']


class AdminSerializer(serializers.ModelSerializer):
    files = UserFilesSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'files')
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'password')
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value.lower()).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return value

    def create(self, validated_data):
        validated_data['username'] = validated_data['username'].lower()
        validated_data['email'] = validated_data['email'].lower()
        validated_data['password'] = make_password(validated_data['password'])
        if 'is_staff' in validated_data:
            validated_data.pop('is_staff')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        if 'username' in validated_data:  # and not request_user.is_staff:
            validated_data.pop('username')
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        if 'is_staff' in validated_data:
            if (not request_user.is_staff or request_user.id == instance.id
                    or instance.is_superuser):
                validated_data.pop('is_staff')
        return super().update(instance, validated_data)

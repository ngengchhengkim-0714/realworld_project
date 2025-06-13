from rest_framework import serializers
from django.conf import settings
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'bio', 'image']

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'bio', 'image']

class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(write_only=True, min_length=8, max_length=32)

  class Meta:
    model = User
    fields = ['email', 'username', 'bio', 'image', 'password']

class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True, write_only=True)
  username = serializers.CharField(read_only=True)

  class Meta:
    model = User
    fields = ['email', 'username', 'bio', 'image', 'password']

  def validate(self, data):
    email = data['email']
    password = data['password']

    user = authenticate(email=email, password=password)
    if not user:
      raise serializers.ValidationError("Invalid username or password.")

    data['user'] = user
    return data

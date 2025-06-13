from rest_framework import serializers
from django.conf import settings
from .models import User
from rest_framework.validators import UniqueValidator


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

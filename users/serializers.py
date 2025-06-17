from rest_framework import serializers
from django.conf import settings
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'bio', 'image']

class UserDetailSerializer(serializers.ModelSerializer):
  token = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = ['username', 'bio', 'image', 'email', 'token']
    read_only_fields = ['token', 'username']

  def get_token(self, user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class ProfileSerializer(serializers.ModelSerializer):
  following = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = ['username', 'bio', 'image', 'following']

  def get_following(self, obj):
    request = self.context.get('request')
    if request and request.user.is_authenticated:
      return obj.followers.filter(id=request.user.id).exists()
    return False

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

  class Meta:
    model = User
    fields = ['email', 'password']

  def validate(self, data):
    email = data['email']
    password = data['password']

    user = authenticate(email=email, password=password)
    if not user:
      raise serializers.ValidationError("Invalid username or password.")

    data['user'] = user
    return data

  def to_representation(self, instance):
    user = self.validated_data['user']
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    return {
      'email': user.email,
      'username': user.username,
      'bio': user.bio,
      'image': user.image,
      'token': token
    }

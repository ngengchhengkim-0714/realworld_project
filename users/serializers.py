from rest_framework import serializers
from django.conf import settings
from .models import User


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'bio', 'image']

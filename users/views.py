from rest_framework import generics
from users.serializers import ProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = ProfileSerializer
  lookup_field = 'username'

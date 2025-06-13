from rest_framework import generics
from users.serializers import ProfileSerializer
from users.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class ProfileView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = ProfileSerializer
  lookup_field = 'username'

class RegisterView(APIView):
  """
  View to handle user registration.
  """
  def post(self, request):
    serializer = RegisterSerializer(data=request.data['user'])
    if serializer.is_valid():
      user = serializer.save()
      refresh = RefreshToken.for_user(user)
      result = serializer.data
      result = {
        'success': True,
        'user': serializer.data
      }
      result['user']['token'] = str(refresh.access_token)

      return Response(result, status=201)
    return Response(serializer.errors, status=400)

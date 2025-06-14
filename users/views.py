from rest_framework import generics, status
from users.serializers import ProfileSerializer
from users.serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

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

      return Response(result, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
  """
  View to handle user login.
  """
  def post(self, request):
    serializer = LoginSerializer(data=request.data['user'])
    if serializer.is_valid():
      user = serializer.data
      refresh = RefreshToken.for_user(serializer.validated_data['user'])

      result = {
        'success': True,
        'user': user
      }
      result['user']['token'] = str(refresh.access_token)

      return Response(result, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = UserSerializer(request.user)
    return Response({'user': serializer.data})

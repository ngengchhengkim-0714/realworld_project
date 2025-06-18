from django.urls import reverse
from rest_framework.test import APIClient

def authenticate_user(self, email, password):
  login_url = reverse('login')
  response = self.client.post(login_url, {
    'user': {
      'email': email,
      'password': password
    }
  }, format='json')

  token = response.data['user']['token']
  return self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from realworld_project.tests.base import authenticate_user

class ProfileAPITestCase(APITestCase):
  def setUp(self):
    email = "admin@test.com"
    password = "password"
    self.user = get_user_model().objects.create_user(username='admin', email=email, password=password)
    self.user2 = get_user_model().objects.create_user(username='user2', email='user2@test.com', password='password')
    authenticate_user(self, email, password)

  def test_retrieval(self):
    url = reverse('profiles-detail', kwargs={'username': 'admin'})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertIn('profile', response.data)

  def test_follow(self):
    url = reverse('profiles-follow', kwargs={'username': self.user2.username})
    response = self.client.post(url)

    self.assertEqual(response.status_code, 200)
    self.assertIn('profile', response.data)
    self.assertTrue(response.data['profile']['following'])

class RegisterAPITestCase(APITestCase):
  def test_post(self):
    url = reverse('register')
    params = {
      'user': {
        'email': 'admin@test.com',
        'username': 'admin',
        'password': 'password',
        'bio': 'bio',
        'image': ''
      }
    }
    response = self.client.post(url, params, format='json')
    data = response.data

    self.assertEqual(response.status_code, 201)
    self.assertIn('user', data)
    self.assertEqual(data['user']['username'], 'admin')
    self.assertEqual(data['user']['bio'], 'bio')
    self.assertEqual(data['user']['image'], '')

class LoginAPITestCase(APITestCase):
  def setUp(self):
    get_user_model().objects.create_user(username='admin', email='admin@test.com', password='password')

  def test_post(self):
    url = reverse('login')
    params = {
      'user': {
        'email': 'admin@test.com',
        'password': 'password'
      }
    }
    response = self.client.post(url, params, format='json')
    data = response.data
    self.assertEqual(response.status_code, 200)
    self.assertIn('user', data)
    self.assertIn('token', data['user'])

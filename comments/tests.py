from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from realworld_project.tests.base import authenticate_user
from articles.models import Article
from comments.models import Comment

class CommentAPITestCase(APITestCase):
  def setUp(self):
    self.user = get_user_model().objects.create_user(
      username='admin',
      password='password',
      email='admin@test.com'
    )
    self.article = Article.objects.create(
      title='Test Article',
      slug='slug',
      description='Test Description',
      body='Test Body',
      author=self.user
    )
    authenticate_user(self, self.user.email, 'password')

  def test_create_comment(self):
    url = reverse('article-comments', kwargs={'slug': self.article.slug})
    params = {
      'comment': {
        'body': 'comment body'
      }
    }
    response = self.client.post(url, params, format='json')
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['body'], 'comment body')

  def test_delete_comment(self):
    comment = Comment.objects.create(
      body='comment body',
      article=self.article,
      author=self.user
    )

    delete_url = reverse('comment-delete', kwargs={'slug': self.article.slug, 'pk': comment.id})
    response = self.client.delete(delete_url)
    self.assertEqual(response.status_code, 204)

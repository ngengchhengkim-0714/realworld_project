from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tags.models import Tag
from django.urls import reverse
from realworld_project.tests.base import authenticate_user
from articles.models import Article

class ArticleAPITestCase(APITestCase):
  def setUp(self):
    email = 'author@test.com'
    password = 'password'
    self.author = get_user_model().objects.create_user(username='author', email=email, password=password)
    self.user1 = get_user_model().objects.create_user(username='user1', email='user1@test.com', password='password1')
    self.tag = Tag.objects.create(name='testtag')
    self.article_params = {
      'title': 'Test Article',
      'body': 'Article body.',
      'description': 'Article description.'
    }

    authenticate_user(self, email, password)

  def test_article_creation(self):
    url = reverse('article-list')
    self.article_params['tag_list'] = [self.tag.id]
    response = self.client.post(url, self.article_params, format='json')
    article = response.data
    self.assertEqual(response.status_code, 201)
    self.assertEqual(article['title'], 'Test Article')
    self.assertEqual(article['body'], 'Article body.')
    self.assertEqual(article['description'], 'Article description.')
    self.assertEqual(article['author']['username'], 'author')
    self.assertEqual(article['tags'][0], self.tag.name)
    self.assertEqual(article['favorited'], False)
    self.assertEqual(article['favoritesCount'], 0)
    self.assertEqual(article['author']['username'], self.author.username)

  def test_article_favorit(self):
    article = Article.objects.create(author=self.author, **self.article_params)
    url = reverse('article-favorite', kwargs={'slug': article.slug})
    response = self.client.post(url)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data['article']['favorited'], True)
    self.assertEqual(response.data['article']['favoritesCount'], 1)

  def test_article_feed(self):
    article = Article.objects.create(author=self.user1, **self.article_params)
    self.author.following.add(self.user1)
    url = reverse('article-feed')
    response = self.client.get(url)
    data = response.data
    self.assertEqual(response.status_code, 200)
    self.assertIn('articles', data)
    self.assertEqual(data['articlesCount'], 1)

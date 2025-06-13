from django.db import models
from django.contrib.auth.models import User
from articles.models import Article
from django.conf import settings

class Comment(models.Model):
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  article = models.ForeignKey(Article, on_delete=models.CASCADE)

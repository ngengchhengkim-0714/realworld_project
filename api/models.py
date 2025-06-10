from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  bio = models.TextField(blank=True, null=True)
  image = models.URLField(blank=True, null=True)

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True)

class Article(models.Model):
  slug = models.SlugField(unique=True)
  title = models.CharField(max_length=255)
  description = models.TextField()
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
  tag_list = models.ManyToManyField(Tag, related_name='articles')

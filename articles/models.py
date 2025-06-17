from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag
from django.conf import settings
from django.utils.text import slugify

class Article(models.Model):
  slug = models.SlugField(unique=True)
  title = models.CharField(max_length=255)
  description = models.TextField()
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  tag_list = models.ManyToManyField(Tag, related_name='articles')
  favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorited_articles', blank=True)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
    super().save(*args, **kwargs)

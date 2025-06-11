from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
from django.contrib.auth import get_user_model

class ArticleViewSet(viewsets.ModelViewSet):
  queryset = Article.objects.all()
  serializer_class = ArticleSerializer
  lookup_field = 'slug'

  def perform_create(self, serializer):
    User = get_user_model()
    user = User.objects.first()
    serializer.save(author=user)

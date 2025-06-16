from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
from django.contrib.auth import get_user_model
from rest_framework import filters

class ArticleViewSet(viewsets.ModelViewSet):
  queryset = Article.objects.all()
  serializer_class = ArticleSerializer
  lookup_field = 'slug'
  filter_backends = [filters.OrderingFilter]
  ordering = ['-created_at']

  def get_queryset(self):
    queryset = super().get_queryset()
    tag_name = self.request.query_params.get('tag')
    author_username = self.request.query_params.get('author')

    if tag_name:
      queryset = queryset.filter(tag_list__name=tag_name)
    if author_username:
      queryset = queryset.filter(author__username=author_username)

    return queryset

  def perform_create(self, serializer):
    User = get_user_model()
    user = User.objects.first()
    serializer.save(author=user)

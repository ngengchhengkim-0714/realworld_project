from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status

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


  @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
  def feed(self, request):
    user = request.user
    offset = int(request.query_params.get('offset', 0))
    limit = int(request.query_params.get('limit', 10))
    articles = Article.objects.filter(author__in=user.following.all()).order_by('-created_at')[offset:offset + limit]
    serializer = self.get_serializer(articles, many=True)
    return Response({
      'articles': serializer.data,
      'articlesCount':
      len(serializer.data)
    })

  @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
  def favorite(self, request, slug=None):
    article = get_object_or_404(Article, slug=slug)

    if article.favorited_by.filter(id=request.user.id).exists():
      article.favorited_by.remove(request.user)
    else:
      article.favorited_by.add(request.user)

    serializer = self.get_serializer(article)
    return Response({
      'article': serializer.data,
    })

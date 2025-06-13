from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404
from .models import Comment, Article
from django.contrib.auth import get_user_model
from .serializers import CommentSerializer

class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer

  def get_article(self):
    return get_object_or_404(Article, slug=self.kwargs['slug'])

  def get_queryset(self):
    return self.queryset.filter(article=self.get_article())

  def perform_create(self, serializer):
    User = get_user_model()
    author = get_object_or_404(User, id=1)
    serializer.save(article=self.get_article(), author=author)

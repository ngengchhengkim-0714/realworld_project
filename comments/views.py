from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404
from .models import Comment, Article
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get_article(self):
    return get_object_or_404(Article, slug=self.kwargs['slug'])

  def get_queryset(self):
    return self.queryset.filter(article=self.get_article())

  def create(self, request, *args, **kwargs):
    article = self.get_article()
    data = request.data.get('comment', {})
    serializer = self.get_serializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(article=article, author=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def destroy(self, request, *args, **kwargs):
    comment = get_object_or_404(Comment, id=kwargs['pk'], article=self.get_article())
    if comment.author != request.user:
      return Response({'error': 'You can only delete your own comments.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

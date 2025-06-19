from rest_framework import viewsets
from .models import Tag
from .serializers import TagSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 10), name='list')
class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()

  serializer_class = TagSerializer

  def get_queryset(self):
    queryset = super().get_queryset()
    print('-----------------------not cache')
    return queryset

from rest_framework import serializers
from .models import Article
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
  tags = serializers.SerializerMethodField(read_only=True)
  tag_list = serializers.ListField(
    child=serializers.CharField(), write_only=True
  )
  author = UserSerializer(read_only=True)

  class Meta:
    model = Article
    fields = ['id', 'title', 'slug', 'description', 'body', 'created_at', 'updated_at', 'author', 'tag_list', 'tags']
    read_only_fields = ['slug']

  def get_tags(self, obj):
    return [tag.name for tag in obj.tag_list.all()]

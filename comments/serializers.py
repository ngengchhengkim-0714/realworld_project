from rest_framework import serializers
from .models import Comment
from users.serializers import ProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
  author = ProfileSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'body', 'created_at', 'updated_at', 'author']

from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """

class ArticleViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows article to be viewed or edited.
  """

class TagViewSet(viewsets.ReadOnlyModelViewSet):
  """
  API endpoint that allows tag to be viewed or edited.
  """

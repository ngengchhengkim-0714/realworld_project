"""
URL configuration for realworld_project project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from articles.views import ArticleViewSet
from tags.views import TagViewSet
from comments.views import CommentViewSet
from users.views import ProfileView
from users.views import RegisterView
from users.views import LoginView

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tag')
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include(router.urls)),
  path('articles/<slug:slug>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='article-comments'),
  path('profiles/<str:username>/', ProfileView.as_view(), name='profile-detail'),
  path('users/', RegisterView.as_view(), name='register'),
  path('users/login', LoginView.as_view(), name='login')
]

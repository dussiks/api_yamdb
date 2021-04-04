from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, generate_code, generate_token,
    GenreViewSet, CategoryViewSet, TitleViewSet,
    ReviewViewSet, CommentViewSet,
)


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review_api')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment_api')

urlpatterns = [
    path('v1/auth/email/', generate_code),
    path('v1/auth/token/', generate_token),
    path('v1/', include(v1_router.urls)),
]

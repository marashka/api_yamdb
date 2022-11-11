from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpView, TitleViewSet, UserViewSet,
                    get_token)

router = DefaultRouter()

router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    'users',
    UserViewSet,
    basename='users'
)

auth_urlpatterns = [
    path(
        'auth/signup/',
        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'auth/token/',
        get_token,
        name='token'
    ),
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(auth_urlpatterns))
]

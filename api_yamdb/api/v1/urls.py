from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    MyTokenObtainPairView, ReviewViewSet, SignUpView,
                    TitleViewSet, UserViewSet)

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

urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/signup/',
        # Урлы с одинаковым префиксом(Auth) выносим в отдельный
        # список, чтобы сделать инклуд

        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'auth/token/',
        MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
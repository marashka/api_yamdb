from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    MyTokenObtainPairView, ReviewViewSet, SignUpView,
                    TitleViewSet, UserViewSet)

router_v1 = DefaultRouter()

router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/signup/',
# Урлы с одинаковым префиксом(Auth) выносим в отдельный 
# список, чтобы сделать инклуд

        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
# Расширяем идею версионинга нашего апи.
# Раньше мы делали это через именование роутера через _v1.
# Но теперь у нас большое приложение. И хранить сериализаторы и вьюсеты и т.д. 
# разных версий в одном файле становится не удобным.
# С этой целью мы можем создавать директории с именем версии апи, 
# которая всебе будет хранить все необходимое для реализации апи, в том числе и файл урлс в 
# котором будут описаны пути.
# В итоге у нас в приложении апи будет несколько папок с версиями апи 
# и корневой файл урлс приложения апи в котором мы будем подключать нужную(нужные) версии апи.

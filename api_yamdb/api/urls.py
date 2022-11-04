from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import CommentViewSet, ReviewViewSet

router_v1 = DefaultRouter()

router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews'
                   )
router_v1.register(r'reviews/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments'
                   )

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/', include('django.contrib.auth.urls')), 
]
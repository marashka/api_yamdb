
from annoying.functions import get_object_or_None
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Genre, Review, Title
from api_yamdb.settings import YAMDB_EMAIL
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminModAuthorOrReadOnly)
from .serializers import (AdminUserSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          MyTokenObtainPairSerializer, ReviewSerializer,
                          SignupSerializer, TitleSerializer, UserSerializer)


User = get_user_model()


class CategoryViewSet(CreateListDestroyViewSet):
    """Админ может создавать категории, остальные только просматривать."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['name', ]
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(CreateListDestroyViewSet):
    """Админ может создавать жанры, остальные только просматривать."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['name', ]
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Админ может создавать тайтлы, остальные только просматривать."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly
                          & IsAdminModAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly
                          & IsAdminModAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(SignupSerializer(data=request.data))
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create_user(**serializer.validated_data)
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = get_object_or_None(User, **serializer.initial_data)
        if user:
            send_confirmation_code(user)
            return Response(
                'Данный пользователь уже зарегистрирован, '
                'сообщение с кодом отправлено на указанную почту',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        if not serializer.validated_data.get('role'):
            serializer.validated_data['role'] = 'user'
        User.objects.create_user(**serializer.validated_data)

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def me_profile(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Код потверждения YaMDb'
    message = f'Код для получения JWT токена: {confirmation_code}'
    recipient_list = (user.email,)
    return send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        from_email=YAMDB_EMAIL
    )

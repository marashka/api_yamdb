from django.shortcuts import get_object_or_404
from rest_framework import mixins, filters, viewsets, generics, status
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from api_yamdb.settings import YMDb_EMAIaL
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, CommentSerializer,
                             ReviewSerializer, SignupSerializer,
                             UserSerializer, MyTokenObtainPairSerializer)
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User
from .filters import TitleFilter


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """Админ может создавать категории, остальные только просматривать."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['name', ]
    # надо сделать пермишны по типу IsAdmin и ReadOnly
    permission_classes = [IsAuthenticatedOrReadOnly]


class GenreViewSet(CreateListDestroyViewSet):
    """Админ может создавать жанры, остальные только просматривать."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['name', ]
    # надо сделать пермишны по типу IsAdmin и ReadOnly
    permission_classes = [IsAuthenticatedOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Админ может создавать тайтлы, остальные только просматривать."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    # надо сделать пермишны по типу IsAdmin и ReadOnly
    permission_classes = [IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # надо сделать пермишны по типу IsAdmin, IsModerator, IsAuthor и ReadOnly
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # надо сделать пермишны по типу IsAdmin, IsModerator, IsAuthor и ReadOnly
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class SignUp(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = User.objects.create_user(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        subject = 'Код потверждения YaMDb'
        message = f'Код для получения JWT токена: {confirmation_code}'
        recipient_list = (user.email,)
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            from_email=YMDb_EMAIaL
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

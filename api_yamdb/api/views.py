from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import mixins, filters, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, CommentSerializer,
                             ReviewSerializer, SignupSerializer,
                             UserSerializer, MyTokenObtainPairSerializer)
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User
from api.permissions import (IsAdmin, IsModerator,
                             IsAuthorOrReadOnly, IsReadOnly)
from api.filters import TitleFilter
from api_yamdb.settings import YMDb_EMAIaL


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
    permission_classes = [IsAdmin | IsReadOnly]


class GenreViewSet(CreateListDestroyViewSet):
    """Админ может создавать жанры, остальные только просматривать."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['name', ]
    permission_classes = [IsAdmin | IsReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Админ может создавать тайтлы, остальные только просматривать."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdmin | IsReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdmin | IsModerator | IsAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdmin | IsModerator | IsAuthorOrReadOnly]

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
    lookup_field = 'username'
    permission_classes = [IsAdmin]

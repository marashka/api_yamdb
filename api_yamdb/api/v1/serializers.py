from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'category', 'genre', 'rating', 'description'
        )

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if rating:
            return round(rating, 1)
        return rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method != 'POST':
            return data

        if Review.objects.filter(
                author=request.user,
                title=title).exists():
            raise serializers.ValidationError(
                'Нельзя сделать 2 отзыва на одно произведение!'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class SignupSerializer(serializers.ModelSerializer):
    # тут добавим валидацию на me и на одинаковость юзернеймов и емейлов.
    # да в модели есть но до нее дойдет после того как дрф все отработает
    # и в итоге мы не отобразим эту ошибку что ме нельзя создавать
    class Meta:
        model = User
        fields = ('username', 'email',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Тут все так сложно выглядит.
    # Можно проще. Тут делаем просто два поля юзернейма и конфирмейшен кода. Чисто для валидации.
    # И создаем обычную апи вьюху на пост метод.
    # И в нем сначала валидируем через этот стерилизатор пришедшие данные.
    # а дальше через отвалидированый юзер нейм тащим из бд юзера и после
    # через чек токен проверяем токен и дальше генерит ему токен и отдаем
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = self.fields.pop('password')

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'confirmation_code': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
# это костыль. так делать нельзя. надо менять логику работы
        self.user = get_object_or_404(User, username=attrs.get('username'))
        if not default_token_generator.check_token(
            self.user,
            authenticate_kwargs['confirmation_code']
        ):
            raise exceptions.ValidationError(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        refresh = self.get_token(self.user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
# по тз возвращается только токен без рефреша
# строго блюдем ТЗ


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

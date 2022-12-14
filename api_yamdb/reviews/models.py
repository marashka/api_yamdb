from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from api_yamdb.settings import TEXT_TITLE_LENGTH
# Нарушен код стайл Джанго.
# Рекомендации Джанго как работать с фалом settings:
# https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#use-of-django-conf-settings

User = get_user_model()


class CreatedModel(models.Model):
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(timezone.now().year)],
        verbose_name='Год выпуска'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Произведения - жанры."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        ordering = ['title', ]

    def __str__(self):
        return f'{self.title} в жанре {self.genre}'


class Review(CreatedModel):
    """Отзывы на произведения"""
    text = models.TextField(
        'Текст'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[MaxValueValidator(10, 'Значение должно быть от 1 до 10.'),
                    MinValueValidator(1, 'Значение должно быть от 1 до 10.')]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True,
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            )
        ]

    def __str__(self):
        return str(self.text[:TEXT_TITLE_LENGTH])


class Comment(CreatedModel):
    """Комментарии к отзывам"""
    text = models.TextField(
        'Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return str(self.text[:TEXT_TITLE_LENGTH])

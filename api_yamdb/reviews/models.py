from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()
TEXT_TITLE_LENGTH = 15


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
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
        max_length=50,
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
    year = models.IntegerField(
        validators=[MaxValueValidator(timezone.now().year), ],
        verbose_name='Год выпуска'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    rating = models.IntegerField(
        null=True,
        default=None,
        verbose_name='Рейтинг'
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
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        ordering = ['title', ]

    def __str__(self):
        return f'{self.title} в жанре {self.genre}'


class Review(models.Model):
    """Отзывы на произведения"""
    text = models.TextField(
        'Текст'
    )
    score = models.IntegerField(
        null=True,
        default=None,
        verbose_name='Оценка',
        validators=[MaxValueValidator(10), MinValueValidator(1)]
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
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.text[:TEXT_TITLE_LENGTH])


class Comment(models.Model):
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
        blank=True,
        null=True,
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return str(self.text[:TEXT_TITLE_LENGTH])

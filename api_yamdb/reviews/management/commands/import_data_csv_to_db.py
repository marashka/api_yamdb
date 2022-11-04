import csv

from django.core.management import BaseCommand

from django.conf import settings
from users.models import User
from reviews.models import (Category, Genre, Title,
                            GenreTitle, Review, Comment)

DATATABLES_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Загрузка данных из файлов .csv в базу данных проекта.'

    def handle(self, *args, **kwargs):
        for model, csv_file in DATATABLES_DICT.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}',
                'r',
                encoding='utf-8'
            ) as file:
                dict_reader = csv.DictReader(file)
                model.objects.bulk_create(
                    model(**data) for data in dict_reader
                )

        self.stdout.write(self.style.SUCCESS('Данные загружены успешно!'))

from django.contrib import admin

from .models import User
# Документация Джанги рекомендует получать  модель User через get_user_model()
# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#referencing-the-user-model

admin.site.register(User)

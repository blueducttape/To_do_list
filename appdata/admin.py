from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


from django.contrib import admin


from .models import Note


@admin.register(Note)
class TodoListAdmin(admin.ModelAdmin):
    # вывод содержимого в листе админки
    list_display = ('title', 'important', 'public', 'status', 'create_at', 'update_at', 'author',)
    # поля только для чтения (неизменяемые поля при редактировании)
    readonly_fields = ('create_at',)
    # фильтры в админке
    list_filter = ('create_at', 'update_at', 'important', 'public', 'status',)


def get_time_plus_day() -> datetime:
    """ Возвращает время + 1 день от текущего """
    return datetime.now()+timedelta(days=1)
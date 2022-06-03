from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


def get_time_plus_day() -> datetime:
    """ Возвращает время + 1 день от текущего """
    return datetime.now()+timedelta(days=1)


class Note(models.Model):

    class Status(models.IntegerChoices):
        """Описание статуса дела"""
        ACTIVE= 1, _('Активная')
        DEFFERED = 0, _('Отложенная')
        DONE = 2, _('Выполнено')

    """Описание одного дела"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(default='', verbose_name='Текст')
    important = models.BooleanField(default=False, verbose_name='Важное дело')
    public = models.BooleanField(default=False, verbose_name='Публичность')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_at = models.DateTimeField(default=get_time_plus_day, verbose_name='Время завершения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', editable=False)
    status = models.IntegerField(default=Status.ACTIVE, choices=Status.choices, verbose_name='Статус')

    def __str__(self):
        return f'Дело №{self.id}'

    class Meta:
        verbose_name = _('Дело')
        verbose_name_plural = _('Дела')

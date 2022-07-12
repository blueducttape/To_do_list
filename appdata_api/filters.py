from typing import Optional
from django.db.models.query import QuerySet


def importance_filter(queryset: QuerySet, importance) -> QuerySet:
    """
    Функция, фильтрующая заметки по полю Важно
    :param queryset: запрос
    :param importance: True или False
    :return: отфильтрованный queryset
    """
    if importance is not None:
        return queryset.filter(importance=importance)
    else:
        return queryset


def public_filter(queryset: QuerySet, public: Optional[bool]) -> QuerySet:
    """
    Функция, фильтрующая заметки по полю Опубликовано
    :param queryset: запрос
    :param public: True или False
    :return: отфильтрованный queryset
    """
    if public is not None:
        return queryset.filter(public=public)
    else:
        return queryset
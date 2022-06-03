from datetime import datetime
from rest_framework import serializers

from appdata.models import Note

class TodolistSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Note

        fields = (
            'id', 'title', 'text', 'create_at', 'update_at', 'status', 'public', 'important',  # из модели
            'author',  # из сериализатора
        )

        read_only_fields = ('create_at',)

    def to_representation(self, instance):
        """ Переопределение вывода. Меняем формат даты в ответе """
        ret = super().to_representation(instance)
        # Конвертируем строку в дату по формату
        create_at = datetime.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # костыль для обработки времени для "времени выполнения"
        try:
            update_at = datetime.strptime(ret['update_at'], '%Y-%m-%dT%H:%M:%SZ')
        except:
            update_at = datetime.strptime(ret['update_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # Конвертируем дату в строку в новом формате
        ret['create_at'] = create_at.strftime('%d %B %Y %H:%M:%S')
        ret['update_at'] = update_at.strftime('%d %B %Y %H:%M:%S')
        return ret
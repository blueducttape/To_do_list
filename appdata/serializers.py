from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note


class AuthorSerializer(serializers.ModelSerializer):
    """ Автор статьи """
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined')


class NoteSerializer(serializers.ModelSerializer):
    """Сериализует все статьи блога"""
    # Меняем вывод, вместо `ID` пользователя будет `Имя`
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ['date_add', 'author']


class NoteDetailSerializer(serializers.ModelSerializer):
    """Сериализует 1 статью блога """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        exclude = ('public',)


class NoteEditorSerializer(serializers.ModelSerializer):
    """ Добавление или изменение статьи """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ['date_add', 'author', ]
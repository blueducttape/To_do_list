
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NoteSerializer, NoteDetailSerializer, NoteEditorSerializer

from .models import Note


def home(request):
    """Домашняя страница для приложения"""
    # Объект, который будет передан в шаблон
    context = {
        "title": "Добро пожаловать!",
        "message": "Это приложение для ведения списка дел",
        "message1": "Регистрация: http://127.0.0.1:8000/api-auth/login/",
        "message2": "Просмотр заметок: http://127.0.0.1:8000/api/v1/notes/"
    }

    return render(request, 'about/index.html', context)


class NoteView(APIView):
    def get(self, request):
        """ Получить список всех записей """
        notes = Note.objects.filter(public=True).order_by('important')
        notes_serializer = NoteSerializer(notes, many=True)
        return Response(notes_serializer.data)


class NoteDetailView(APIView):
    """Получить 1 статью"""
    def get(self, request, note_id):
        note = Note.objects.filter(pk=note_id, public=True).first()

        if not note:
            raise NotFound(f'Опубликованная статья с id={note_id} не найдена')

        serializer = NoteDetailSerializer(note)
        return Response(serializer.data)

    def delete(self, request, note_id):
        """Метод для удаления статьи"""
        note = Note.objects.filter(pk=note_id).first()

        if not note:
            raise NotFound(f'Cтатья с id={note_id} не найдена')

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteEditorView(APIView):
    """ Добавление или изменение статьи """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """ Новая статья для блога """
        # Передаем в сериалайзер (валидатор) данные из запроса
        new_note = NoteEditorSerializer(data=request.data)
        # Проверка параметров
        if new_note.is_valid():
            # Записываем новую статью и добавляем текущего пользователя как автора
            new_note.save(author=request.user)
            return Response(new_note.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, note_id):
        # Находим редактируемую статью
        note = Note.objects.filter(pk=note_id, author=request.user).first()
        if not note:
            raise NotFound(f'Статья с id={note_id} для пользователя {request.user.username} не найдена')

        new_note = NoteEditorSerializer(note, data=request.data, partial=True)

        if new_note.is_valid():
            new_note.save()
            return Response(new_note.data, status=status.HTTP_200_OK)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

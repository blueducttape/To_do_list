from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from appdata.models import Note
from . import serializers, filters, permissions


class TodoListApiView(APIView):
    """
    Представление, которое позволяет вывести весь список дел и добавить новую запись.
    Выводит записи всех пользователей, вне зависимости от статуса, публичности и т.д.
    работа через url: all_cases
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        """Вывод всех дел"""
        objects = Note.objects.all()
        serializer = serializers.TodolistSerializer(
            instance=objects,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request: Request):
        """Добавление записи через json"""
        serializer = serializers.TodolistSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class TodoOnceView(APIView):
    """
    Представление для работы с единичной записью
    Доступ к записи - по ключу, работа через url: case/int
    """
    permission_classes = (IsAuthenticated, permissions.OnlyAuthorEditTask)

    def change_body_case(self, pk: int, partial: bool) -> Response:
        """Выполнение частичного или полного обновления полей"""
        instance = self.check_constraint(pk)
        serializer = serializers.TodolistSerializer(instance=instance,  # объект с которым работаем
                                                    data=self.request.data,  # данные из браузера
                                                    partial=partial)
        if serializer.is_valid(True):  # проверка данных с разрешением вызова исключений
            serializer.save()  # сохранение данных
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def check_constraint(self, pk: int):
        """Проверка по ограничениям"""
        instance = get_object_or_404(Note, pk=pk)
        self.check_object_permissions(self.request, instance)
        return instance

    def get(self, request: Request, pk: int) -> Response:
        """Отображение заданной записи по заданному ключу"""
        instance = self.check_constraint(pk)
        serializer = serializers.TodolistSerializer(instance=instance)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Response:
        """Полное обновление записи по ключу"""
        return self.change_body_case(pk=pk, partial=False)

    def patch(self, request: Request, pk: int) -> Response:
        """Частичное обновление записи по ключу"""
        return self.change_body_case(pk=pk, partial=True)


    def delete(self, request: Request, pk: int) -> Response:
        """ удаление записи по ключу"""
        queryset = get_object_or_404(Note, pk=pk)
        self.check_object_permissions(request, queryset)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TodoListCreateAPIView(generics.ListCreateAPIView):
    """
    Представление через generic, вывод отсортированных записей
    сортировка по дате, затем по важности
    работа через url: cases
    """
    queryset = Note.objects.all()
    serializer_class = serializers.TodolistSerializer
    permission_classes = (IsAuthenticated,)

    ordering = ["important", "update_at"]  # поля для сортировки

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.order_by_queryset(queryset)
        return queryset

    def order_by_queryset(self, queryset: queryset):
        """ Сортировка заметок по дате, затем по важности."""
        return queryset.order_by(*self.ordering)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # добавили автора для сохранения


class TodoPublicListApiView(generics.ListAPIView):
    """
    Представление для отображения только публичных записей для
    авторизованных пользователей, сортировка по времени,
    """
    queryset = Note.objects.all()
    serializer_class = serializers.TodolistSerializer
    permission_classes = (IsAuthenticated,)  # запрещаем неавторизованных пользователей

    def get_queryset(self):

        queryset = super().get_queryset()
        return queryset.filter(public=True).order_by("-create_at")


class TodoListFilterApiView(generics.ListAPIView):
    """
    Представление для отображения записей с импользованием фильтров
    public - True / False  - отметка публичности
    important - True / False - отметка важности
    status - отметка о сотоянии:
        0 - отложено,
        1 - активна,
        2 - выполена
    работа по url: filter_cases/
    """
    queryset = Note.objects.all()
    serializer_class = serializers.TodolistSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):

        important = self.request.query_params.get('important')
        queryset = filters.importance_filter(queryset, important)

        stat = self.request.query_params.getlist('status')
        queryset = filters.public_filter(queryset, stat)

        return queryset


class TodoEditViaGeneric(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для редактирования единичной записи
    работа по url: /edit_case/<int>
    """
    queryset = Note.objects.all()
    serializer_class = serializers.TodolistSerializer
    # запрещаем неавторизованным доступ, не авторам - редактирование
    permission_classes = (IsAuthenticated, permissions.OnlyAuthorEditTask)

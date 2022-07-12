from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from appdata_api.views import *
from appdata_api.models import Note

User = get_user_model()


class TestTaskRetrieveUpdateDestroyAPIView(APITestCase):
    USER_1 = dict(
        username="someuser1",
        password="fake_password",
    )
    USER_2 = dict(
        username="someuser2",
        password="fake_password",
    )

    @classmethod
    def setUpTestData(cls):

        users = [
            User(**cls.USER_1),
            User(**cls.USER_2),
        ]
        User.objects.bulk_create(users)
        cls.db_user_1 = users[0]

        notes = [
            Note(title="title_1", author=users[0]),
            Note(title="title_2", author=users[1]),
        ]
        Note.objects.bulk_create(notes)

    def setUp(self) -> None:
        """При каждом тестовом методе, будем делать нового клиента и авторизовать его."""
        self.auth_user_1 = APIClient()
        self.auth_user_1.force_authenticate(user=self.db_user_1)


    def test_get(self):
        """Автор видит конкретную свою запись любую"""

        note_pk = 1
        url = f"/api/v1/notes/{note_pk}/"
        resp = self.auth_user_1.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_note(self):
        """Автор видит конкретную чужую публичную запись"""

        other_note_pk = 2
        url = f"/api/v1/notes/{other_note_pk}/"
        resp = self.auth_user_1.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_forbidden(self):
        """Автор не видит непубличную запись"""

        note_pk = 2
        data = {
            "title": "fake_title",
            "public": False
        }
        url = f"/api/v1/notes/{note_pk}/"
        resp = self.auth_user_1.get(url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


    def test_partial_update_other_note(self):
        """Автор может изменить свою запись"""

        note_pk = 1
        url = f"/api/v1/notes/{note_pk}/"
        resp = self.auth_user_1.patch(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_update_other_note(self):
        """Автор не может изменить чужую запись (публичную, непубличную)"""

        note_pk = 2
        data = {
            "title": "fake_title",
        }
        url = f"/api/v1/notes/{note_pk}/"
        resp = self.auth_user_1.patch(url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)



    def test_delete(self):
        """Автор может удалить свою запись"""

        note_pk = 1
        data = {
            "title": "fake_title",
        }
        url = f"/api/v1/notes/{note_pk}/"
        resp = self.auth_user_1.delete(url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_other_note(self):
        """Автор не может удалить чужую запись"""

        note_pk = 2
        data = {
            "title": "fake_title",
        }
        url = f"/api/v1/notes/{note_pk}/"
        resp = self.auth_user_1.delete(url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

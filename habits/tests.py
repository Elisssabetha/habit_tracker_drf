from rest_framework.test import APITestCase
from django.urls import reverse
from habits.models import Habit
from users.models import User
from rest_framework import status


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com', is_staff=True, is_superuser=True)
        self.user.set_password('1234')
        self.user.save()

        response = self.client.post(
            '/users/token/',
            {'email': 'test@test.com', 'password': "1234"}
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.data = {
            "place": "Дома",
            "time": "2023-09-23 16:12",
            "action": "Тестовая привычка",
            "execution_time": "00:01:30",
        }

    def test_create_habit(self):
        response = self.client.post(
            reverse('habits:habits_create'),
            self.data
        )
        pk = Habit.objects.all().latest('pk').pk
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "place": "Дома",
                "time": "2023-09-23T16:12:00Z",
                "action": "Тестовая привычка",
                "is_pleasant": False,
                "frequency": 1,
                "reward": None,
                "execution_time": "00:01:30",
                "is_public": False,
                "user": self.user.pk,
                "related_habit": None
            }
        )

    def test_list_habit(self):
        self.test_create_habit()
        response = self.client.get(reverse('habits:habits_list'))
        pk = Habit.objects.all().latest('pk').pk
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['results'],
            [
                {
                    "id": pk,
                    "place": "Дома",
                    "time": "2023-09-23T16:12:00Z",
                    "action": "Тестовая привычка",
                    "is_pleasant": False,
                    "frequency": 1,
                    "reward": None,
                    "execution_time": "00:01:30",
                    "is_public": False,
                    "user": self.user.pk,
                    "related_habit": None
                }
            ]
        )

    def test_list_public_habit(self):
        response = self.client.get(reverse('habits:public_habits_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_retrieve_habit(self):
        self.test_create_habit()
        pk = Habit.objects.all().latest('pk').pk
        response = self.client.get(f'/habits/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "place": "Дома",
                "time": "2023-09-23T16:12:00Z",
                "action": "Тестовая привычка",
                "is_pleasant": False,
                "frequency": 1,
                "reward": None,
                "execution_time": "00:01:30",
                "is_public": False,
                "user": self.user.pk,
                "related_habit": None
            }
        )

    def test_update_habit(self):
        self.test_create_habit()
        pk = Habit.objects.all().latest('pk').pk
        response = self.client.patch(f'/habits/update/{pk}/', {'place': 'Test place'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "place": "Test place",
                "time": "2023-09-23T16:12:00Z",
                "action": "Тестовая привычка",
                "is_pleasant": False,
                "frequency": 1,
                "reward": None,
                "execution_time": "00:01:30",
                "is_public": False,
                "user": self.user.pk,
                "related_habit": None
            }
        )

    def test_destroy_habit(self):
        self.test_create_habit()
        pk = Habit.objects.all().latest('pk').pk
        response = self.client.delete(f'/habits/delete/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

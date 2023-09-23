from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = '/users/user/'
        self.data = {
            'email': 'test@test.ru',
            'password': 'test'
        }

    def test_create_user(self):
        """User creation testing """

        response = self.client.post(f'{self.url}', data=self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                'email': 'test@test.ru',
                'password': 'test',
            }
        )

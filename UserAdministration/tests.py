from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from UserAdministration.models import UserProfile
from pprint import pprint


class ViewTestCase(TestCase):
    """ Tests User Profile Model"""

    def setUp(self):
        self.client = APIClient()

    def test_api_can_create_user_and_user_profile(self):
        data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "email": "a@gmail.com"
        }

        self.response = self.client.post(
            reverse('rest_register'),
            data,
            format='json'
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserProfile.objects.all().count(), 1)

    def test_api_can_update_user_and_profile(self):
        """
        Tests whether a user profile can be updated via patch method or not.
        :return:
        """
        user = User.objects.create(username='akhan', password='test1234', email='akhan@gmail.com')
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        data = {
            'user': {
                'first_name': 'adnan',
                'last_name': 'khan',
            },
            'bio': 'Updated-Bio-test',
            'location': 'Bangladesh'
        }

        self.response = self.client.patch(
            reverse('userprofile-detail', kwargs={'pk': user.profile.id}),
            data,
            format='json'
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_profile_only(self):
        user = User.objects.create(username='akhan', password='test1234', email='akhan@gmail.com')
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        data = {
            'bio': 'Updated-Bio-test',
            'location': 'Bangladesh'
        }

        self.response = self.client.patch(
            reverse('userprofile-detail', kwargs={'pk': user.profile.id}),
            data,
            format='json'
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_user_only(self):
        user = User.objects.create(username='akhan', password='test1234', email='akhan@gmail.com')
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        data = {
            'user': {
                'first_name': 'adnan',
                'last_name': 'khan',
            }
        }

        self.response = self.client.patch(
            reverse('userprofile-detail', kwargs={'pk': user.profile.id}),
            data,
            format='json'
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_user_and_profile(self):
        user = User.objects.create(username='akhan', password='test1234', email='akhan@gmail.com')
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        self.response = self.client.delete(
            reverse('userprofile-detail', kwargs={'pk': user.profile.id}),
            format='json',
            follow=True
        )

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        pass

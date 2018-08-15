from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from LikeApp.models import UserToUserModel


# Create your tests here.

class UserToUserRelationTestCase(TestCase):
    """ Tests User Profile Model"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_user_can_like_another_user(self):
        user_1 = User.objects.create(username="user_to_like_1", password="test1234", email="like2@gmail.com")

        data = {
            'username': user_1.username,
        }

        self.response = self.client.post(
            reverse("user-like-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unlike_another_user(self):
        user_1 = User.objects.create(username="user_to_like1", password="test1234", email="like2@gmail.com")
        obj=UserToUserModel.objects.create(base_user=self.user, activity_type=UserToUserModel.LIKE, user=user_1)

        data ={
            'user_id': user_1.id,
            'username': user_1.username
        }

        self.response = self.client.post(
            reverse("user-like-remove"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_user_can_save_another_user(self):
        user_1 = User.objects.create(username="user_to_save_1", password="test1234", email="like2@gmail.com")

        data = {
            'username': user_1.username
        }

        self.response = self.client.post(
            reverse("user-save-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unsave_another_user(self):
        user_1 = User.objects.create(username="user_to_save1", password="test1234", email="like2@gmail.com")
        UserToUserModel.objects.create(base_user=self.user, activity_type=UserToUserModel.SAVE, user=user_1)
        data = {
            'user_id': user_1.id,
            'username': user_1.username
        }

        self.response = self.client.post(
            reverse("user-save-remove"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.client.logout()

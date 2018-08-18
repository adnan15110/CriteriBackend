from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from FollowWatchApp.models import UserToUserModel


# Create your tests here.

class UserToUserRelationTestCase(TestCase):
    """ Tests User Profile Model"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_user_can_follow_another_user(self):
        user_1 = User.objects.create(username="user_to_follow_1", password="test1234", email="like2@gmail.com")

        data = {
            'username': user_1.username,
        }

        self.response = self.client.post(
            reverse("user-follow-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unfollow_another_user(self):
        user_1 = User.objects.create(username="user_to_follow1", password="test1234", email="like2@gmail.com")
        obj=UserToUserModel.objects.create(base_user=self.user, activity_type=UserToUserModel.FOLLOW, user=user_1)

        data ={
            'user_id': user_1.id,
            'username': user_1.username
        }

        self.response = self.client.post(
            reverse("user-follow-remove"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_user_can_watch_another_user(self):
        user_1 = User.objects.create(username="user_to_watch_1", password="test1234", email="like2@gmail.com")

        data = {
            'username': user_1.username
        }

        self.response = self.client.post(
            reverse("user-watch-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unwatch_another_user(self):
        user_1 = User.objects.create(username="user_to_watch1", password="test1234", email="like2@gmail.com")
        UserToUserModel.objects.create(base_user=self.user, activity_type=UserToUserModel.WATCH, user=user_1)
        data = {
            'user_id': user_1.id,
            'username': user_1.username
        }

        self.response = self.client.post(
            reverse("user-watch-remove"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.client.logout()

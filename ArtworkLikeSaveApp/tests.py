from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ArtworkLikeSaveApp.models import UserToArtworkModel
from Art.models import Artwork


# Create your tests here.

class UserToArtworkRelationTestCase(TestCase):
    """ Tests User Profile Model"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        artwork_data = {
            # 'artwork_image': ''
            'width': 100,
            'height': 300,
            'unit': 'inch',
            'description': 'Artwork description',
            'title': 'Rural Landscape',

        }
        self.artwork = Artwork.objects.create(**artwork_data, user=self.user)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_user_can_like_artwork(self):

        data = {
            'artwork_id': self.artwork.id,
            'artwork_title': self.artwork.title,
        }

        self.response = self.client.post(
            reverse("user-like-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unlike_artwork(self):
        UserToArtworkModel.objects.create(user=self.user, activity_type=UserToArtworkModel.LIKE, artwork=self.artwork)
        data = {
            'artwork_id': self.artwork.id,
            'artwork_title': self.artwork.title,
        }

        self.response = self.client.post(
            reverse("user-like-remove"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_user_can_save_an_artwork(self):
        data = {
            'artwork_id': self.artwork.id,
            'artwork_title': self.artwork.title,
        }

        self.response = self.client.post(
            reverse("user-save-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unsave_an_artwork(self):
        UserToArtworkModel.objects.create(user=self.user, activity_type=UserToArtworkModel.SAVE, artwork=self.artwork)

        data = {
            'artwork_id': self.artwork.id,
            'artwork_title': self.artwork.title,
        }
        self.response = self.client.post(
            reverse("user-save-remove"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.client.logout()

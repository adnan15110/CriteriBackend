from django.test import TestCase
from unittest import skip
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from UserAdministration.models import Profile
from pprint import pprint
from django.conf import settings
import os


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
            reverse("rest_register"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(Profile.objects.all().count(), 1)

    def test_api_get_user_profile(self):
        user_1 = User.objects.create(username="akhan1", password="test12345", email="akhan1@gmail.com")
        user_2 = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=user_2)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

        self.response = self.client.get(
            reverse("profile-list"),
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data), 1)

    def test_api_can_update_user_and_profile(self):
        """
        Tests whether a user profile can be updated via patch method or not.
        :return:
        """
        user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

        data = {
            "user": {
                "first_name": "adnan",
                "last_name": "khan",
            },
            "address": {
                "apt_number": 678,
                "street_number": 77,
                "street_name": "University Crescent",
                "neighbourhood": "",
                "city": "Winnipeg",
                "province": "Manitoba",
                "postal_code": "R3T3N8",
                "country": "Canada"
            },
            "headline": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "biography": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibul",
            "website": "www.test.com",
            "date_of_birth": "1988-03-01",
            "profile_level": "ProfilePlus"
        }

        self.response = self.client.patch(
            reverse("profile-detail", kwargs={"pk": user.profile.id}),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    @skip("skipping the image upload test")
    def test_api_can_upload_profile_images(self):
        image_path = os.path.join(settings.TEST_DATA_DIR, "profile.png")
        file = open(image_path, "rb")
        small_image_path = os.path.join(settings.TEST_DATA_DIR, "small.png")
        small_image_file = open(small_image_path, "rb")

        user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

        data = {
            "small_profile_image": file,
            "large_profile_image": small_image_file
        }
        response = self.client.patch(reverse("profile-detail", kwargs={"pk": user.profile.id}), data,
                                     format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_update_profile_only(self):
        user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

        data = {
            "headline": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "biography": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            "website": "www.test.com",
            "date_of_birth": "1988-03-01",
            "profile_level": "ProfilePlus"
        }

        self.response = self.client.patch(
            reverse("profile-detail", kwargs={"pk": user.profile.id}),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_address_only(self):
        user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

        data = {
            "address": {
                "apt_number": 678,
                "street_number": 77,
                "street_name": "University Crescent",
                "neighbourhood": "",
                "city": "Winnipeg",
                "province": "Manitoba",
                "postal_code": "R3T3N8",
                "country": "Canada"
            }
        }

        self.response = self.client.patch(
            reverse("profile-detail", kwargs={"pk": user.profile.id}),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_update_user_only(self):
        user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

        data = {
            "user": {
                "first_name": "adnan",
                "last_name": "khan"
            }
        }

        self.response = self.client.patch(
            reverse("profile-detail", kwargs={"pk": user.profile.id}),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_user_and_profile(self):
        user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

        self.response = self.client.delete(
            reverse("profile-detail", kwargs={"pk": user.profile.id}),
            format="json",
            follow=True
        )

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        pass

from django.test import TestCase
from unittest import skip
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from Art.models import ArtCategory, Artwork, ArtCollection


class ArtCategoryApiTestCase(TestCase):
    """ Tests User Profile Model"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    # ART CATEGORY
    def test_api_can_create_category(self):
        """
        creates art category.
        :return:
        """
        data = {
            'category_name': 'Painting',
            'details': 'painting category'
        }

        self.response = self.client.post(
            reverse("art-category-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_update_category(self):
        """
            creates art category.
            :return:
        """
        category = ArtCategory.objects.create(category_name='Drawing', details='Drawing details')

        data = {
            'category_name': 'Painting',
            'details': 'painting category'
        }

        self.response = self.client.patch(
            reverse("art-category-detail", kwargs={"pk": category.id}),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_category(self):
        """
        creates art category.
        :return:
        """
        category = ArtCategory.objects.create(category_name='Drawing', details='Drawing details')

        self.response = self.client.delete(
            reverse("art-category-detail", kwargs={"pk": category.id}),
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.client.logout()

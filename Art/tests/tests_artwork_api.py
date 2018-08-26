from django.test import TestCase
from unittest import skip
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from Art.models import ArtCategory, Artwork, ArtCollection


class ArtworkApiTestCase(TestCase):
    """ Tests User Profile Model"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    # ARTWORK
    def test_api_can_create_artwork(self):
        data = {
            # "artwork_image": ""
            "width": 100,
            "height": 300,
            "unit": "inch",
            "description": "Artwork description",
            "categories": [],
            "title": "Rural Landscape",

        }
        self.response = self.client.post(
            reverse("artwork-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_artwork_with_category(self):
        categories = [
            {
                "category_name": "Painting",
                "details": "painting category"
            },
            {
                "category_name": "Architecture",
                "details": "Architecture"
            },
            {
                "category_name": "Oil Painting",
                "details": "Oil painting"
            },
        ]

        for cat in categories:
            ArtCategory.objects.create(**cat)

        data = {
            # "artwork_image": ""
            "categories": [],
            "width": 100,
            "height": 300,
            "unit": "inch",
            "description": "Artwork description",
            "categories": [],
            "title": "Rural Landscape",
        }
        self.response = self.client.post(
            reverse("artwork-list"),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_update_artwork(self):
        artwork = Artwork.objects.create(user=self.user, title="Rural Landscape", description="Drawing details")

        data = {
            # "artwork_image": ""
            "width": 100,
            "height": 300,
            "unit": "inch",
            "description": "Artwork description",
        }

        self.response = self.client.patch(
            reverse("artwork-detail", kwargs={"pk": artwork.id}),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_artwork(self):
        artwork = Artwork.objects.create(user=self.user, title="Rural Landscape", description="Drawing details")

        self.response = self.client.delete(
            reverse("artwork-detail", kwargs={"pk": artwork.id}),
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_can_update_artwork_with_category(self):
        artwork = Artwork.objects.create(user=self.user, title="Rural Landscape", description="Drawing details")
        categories = [
            {
                "category_name": "Painting",
                "details": "painting category"
            },
            {
                "category_name": "Architecture",
                "details": "Architecture"
            },
            {
                "category_name": "Oil Painting",
                "details": "Oil painting"
            },
        ]

        for cat in categories:
            ArtCategory.objects.create(**cat)

        data = {
            # "artwork_image": ""
            "dimension": "100x100 inch",
            "description": "Artwork description",
            "categories": [{"category_name": "Painting"}, {"category_name": "Architecture"}]
        }
        self.response = self.client.patch(
            reverse("artwork-detail", kwargs={"pk": artwork.id}),
            data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    #  CATEGORY ADD REMOVE TEST
    def test_api_can_add_category_to_artwork(self):
        data = {
            # "artwork_image": ""
            "width": 100,
            "height": 300,
            "unit": "inch",
            "description": "Artwork description",
            "title": "Rural Landscape",

        }
        artwork = Artwork.objects.create(**data, user=self.user)
        artwork.save()

        categories = [
            {
                "category_name": "Painting",
                "details": "painting category"
            },
            {
                "category_name": "Architecture",
                "details": "Architecture"
            },
            {
                "category_name": "Oil Painting",
                "details": "Oil painting"
            },
        ]

        category_objs = []

        for cat in categories:
            obj = ArtCategory.objects.create(**cat)
            category_objs.append(obj)

        category_data = [
            {
                "id": category_objs[0].id,
                "category_name": category_objs[0].category_name
            },
            {
                "id": category_objs[1].id,
                "category_name": category_objs[1].category_name
            },
            {
                "id": category_objs[2].id,
                "category_name": category_objs[2].category_name
            },
        ]

        self.response = self.client.post(
            reverse("artwork-add-to-categories", kwargs={"pk": artwork.id}),
            category_data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_add_category_to_artwork_with_existing_category(self):
        data = {
            # "artwork_image": ""
            "width": 100,
            "height": 300,
            "unit": "inch",
            "description": "Artwork description",
            "title": "Rural Landscape",

        }
        artwork = Artwork.objects.create(**data, user=self.user)
        artwork.save()

        categories = [
            {
                "category_name": "Painting",
                "details": "painting category"
            },
            {
                "category_name": "Architecture",
                "details": "Architecture"
            },
            {
                "category_name": "Oil Painting",
                "details": "Oil painting"
            },
        ]

        category_objs = []

        for cat in categories:
            obj = ArtCategory.objects.create(**cat)
            category_objs.append(obj)

        # add one programmatically
        artwork.categories.add(category_objs[0])

        category_data = [
            {
                "id": category_objs[1].id,
                "category_name": category_objs[1].category_name
            },
            {
                "id": category_objs[2].id,
                "category_name": category_objs[2].category_name
            },
        ]

        self.response = self.client.post(
            reverse("artwork-add-to-categories", kwargs={"pk": artwork.id}),
            category_data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_category_from_artwork(self):

        data = {
            # "artwork_image": ""
            "width": 100,
            "height": 300,
            "unit": "inch",
            "description": "Artwork description",
            "title": "Rural Landscape",

        }
        artwork = Artwork.objects.create(**data, user=self.user)
        artwork.save()

        categories = [
            {
                "category_name": "Painting",
                "details": "painting category"
            },
            {
                "category_name": "Architecture",
                "details": "Architecture"
            },
            {
                "category_name": "Oil Painting",
                "details": "Oil painting"
            },
        ]

        category_obj = []

        for cat in categories:
            obj = ArtCategory.objects.create(**cat)
            category_obj.append(obj)
            artwork.categories.add(obj)

        category_data = [
            {
                "id": category_obj[1].id,
                "category_name": category_obj[1].category_name
            },
            {
                "id": category_obj[2].id,
                "category_name": category_obj[2].category_name
            },
        ]

        self.response = self.client.post(
            reverse("artwork-delete-from-categories", kwargs={"pk": artwork.id}),
            category_data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(artwork.categories.count(), 1)

    def tearDown(self):
        self.client.logout()

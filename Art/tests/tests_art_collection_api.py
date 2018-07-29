from django.test import TestCase
from unittest import skip
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from Art.models import ArtCategory, Artwork, ArtCollection


class ArtCollectionTestCase(TestCase):
    """ Tests User Profile Model"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    # ARTWORK COLLECTION
    def test_api_can_create_artwork_collection(self):
        data = {
            'title': 'My Personal Collection',
            'description': 'Collection of my Artwork',
            'artworks': []
        }

        self.response = self.client.post(
            reverse("art-collection-list"),
            data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_update_artwork_collection(self):
        collection = ArtCollection.objects.create(title='my art collection', user=self.user)
        collection.save()
        data = {
            'title': 'My Personal Collection --updated',
        }

        self.response = self.client.put(
            reverse("art-collection-detail", kwargs={"pk": collection.id}),
            data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_artwork_collection(self):
        collection = ArtCollection.objects.create(title='my art collection', user=self.user)
        collection.save()

        self.response = self.client.delete(
            reverse("art-collection-detail", kwargs={"pk": collection.id}),
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    # add Artwork to Collection
    def test_api_can_add_artwork_to_collection(self):
        data = {
            # 'artwork_image': ''
            'width': 100,
            'height': 300,
            'unit': 'inch',
            'description': 'Artwork description',
            'title': 'Rural Landscape',

        }
        artwork = Artwork.objects.create(**data, user=self.user)
        artwork.save()

        artwork1 = Artwork.objects.create(**data, user=self.user)
        artwork1.save()

        collection = ArtCollection.objects.create(title='my art collection', user=self.user)
        collection.save()
        collection_data = [
            {
                'id': artwork.id,
                'title': artwork.title
            },
            {
                'id': artwork1.id,
                'title': artwork1.title
            }
        ]

        self.response = self.client.post(
            reverse("art-collection-add-to-collection", kwargs={"pk": collection.id}),
            collection_data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_add_artwork_to_collection_with_existing_artwork(self):
        data = {
            # 'artwork_image': ''
            'width': 100,
            'height': 300,
            'unit': 'inch',
            'description': 'Artwork description',
            'title': 'Rural Landscape',

        }
        artwork = Artwork.objects.create(**data, user=self.user)
        artwork.save()

        artwork1 = Artwork.objects.create(**data, user=self.user)
        artwork1.save()

        collection = ArtCollection.objects.create(title='my art collection', user=self.user)
        collection.save()
        collection.artworks.add(artwork1)

        collection_data = [
            {
                'id': artwork.id,
                'title': artwork.title
            },
        ]

        self.response = self.client.post(
            reverse("art-collection-add-to-collection", kwargs={"pk": collection.id}),
            collection_data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_artwork_from_collection(self):
        data = {
            # 'artwork_image': ''
            'width': 100,
            'height': 300,
            'unit': 'inch',
            'description': 'Artwork description',
            'title': 'Rural Landscape',

        }
        artwork = Artwork.objects.create(**data, user=self.user)
        artwork.save()

        artwork1 = Artwork.objects.create(**data, user=self.user)
        artwork1.save()

        collection = ArtCollection.objects.create(title='my art collection', user=self.user)
        collection.save()
        collection.artworks.add(artwork1, artwork)

        collection_data = [
            {
                'id': artwork1.id,
                'title': artwork1.title
            }
        ]

        self.response = self.client.post(
            reverse("art-collection-delete-from-collection", kwargs={"pk": collection.id}),
            collection_data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(collection.artworks.count(), 1)

    def tearDown(self):
        self.client.logout()

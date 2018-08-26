from django.test import TestCase
from unittest import skip
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from Report.models import ArtworkReport
from Art.models import Artwork


class ReportApiTestCase(TestCase):
    """ Tests User Profile Model"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="akhan", password="test1234", email="akhan@gmail.com")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.key))

    def test_api_test_main_feed_view(self):
        self.assertEqual(1, 1)

    def tearDown(self):
        self.client.logout()
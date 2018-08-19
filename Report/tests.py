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

        params = {
            # 'artwork_image': ''
            'width': 100,
            'height': 300,
            'unit': 'inch',
            'description': 'Artwork description',
            'title': 'Rural Landscape',

        }
        self.artwork = Artwork.objects.create(**params, user=self.user)

    def test_api_can_create_report(self):
        data = {
            'artwork': reverse('artwork-detail', kwargs={'pk': self.artwork.id}),
            'report_type': ArtworkReport.INAPPROPRIATE_CONTENT,
            'report_status': ArtworkReport.PENDING,
            'Description': 'desc',
        }
        self.response = self.client.post(
            reverse("artwork-report-list"),
            data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_update_report(self):
        params = {
            'report_type': ArtworkReport.INAPPROPRIATE_CONTENT,
            'report_status': ArtworkReport.PENDING,
            'description': 'desc',
        }
        report= ArtworkReport.objects.create(**params, artwork=self.artwork, reporter=self.user)
        data = {
            'report_status':ArtworkReport.REVIEWED,
        }
        self.response = self.client.patch(
            reverse("artwork-report-detail", kwargs={'pk': report.id}),
            data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_report(self):
        params = {
            'report_type': ArtworkReport.INAPPROPRIATE_CONTENT,
            'report_status': ArtworkReport.PENDING,
            'description': 'desc',
        }
        report = ArtworkReport.objects.create(**params, artwork=self.artwork, reporter=self.user)

        self.response = self.client.delete(
            reverse("artwork-report-detail", kwargs={"pk": report.id}),
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.client.logout()
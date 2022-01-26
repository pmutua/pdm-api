from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from  pdm.apps.demographics.models import (
    District,
)
from  pdm.apps.demographics.serializers import (
    DistrictSerializer
)
from .factories import (
    DistrictFactory
)

# initialize the APIClient app
client = APIClient()


class PostCreateDistrictTest(APITestCase):
    """Test module for POST add new user API"""

    def setUp(self):
        self.district = DistrictFactory.create()

    def test_post_district_created(self):
        url = reverse("districts")
        data = {
            "name": "PADER"
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


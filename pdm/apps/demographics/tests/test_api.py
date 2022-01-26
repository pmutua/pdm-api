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
    DistrictFactory,
    CountyFactory,
    SubCountyFactory,
    ParishFactory,
    VillageFactory
)

# initialize the APIClient app
client = APIClient()

class PostDemographicsTest(APITestCase):
    """Test module for POST add new user API"""

    def setUp(self):
        self.district = DistrictFactory.create()
        self.county = CountyFactory.create()
        self.subcounty = SubCountyFactory.create()
        self.parish = ParishFactory.create()
        self.village = VillageFactory.create()

    # TODO TEST invalid payload
    # POST METHODS
    def test_post_district_created(self):
        url = reverse("districts")
        data = {
            "name": "PADER"
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_county_created(self):
        url = reverse("counties")
        data = {
            "name": "PADER",
            "district": self.district.id
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_sub_county_created(self):
        url = reverse("sub-counties")
        data = {
            "name": "PADER",
            "county": self.county.id
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_parish_created(self):
        url = reverse("parishes")
        data = {
            "name": "PADER",
            "sub_county": self.subcounty.id
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_village_created(self):
        url = reverse("villages")
        data = {
            "name": "PADER",
            "parish": self.parish.id
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # GET METHODS
    def test_get_district_detail(self):
        url = reverse("district-detail", kwargs={'pk': self.district.pk})
        response = client.get(url, format="json")
        self.assertEqual(DistrictSerializer(self.district).data,response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


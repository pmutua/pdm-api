from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from pdm.apps.farmers.serializers import (
    FarmerDetailSerializer
)

from pdm.apps.demographics.tests.factories import (
    DistrictFactory,
    CountyFactory,
    SubCountyFactory,
    ParishFactory,
    VillageFactory
)

# initialize the APIClient app
client = APIClient()


class PostFarmersAPITest(APITestCase):
    """Test module for POST add new user API"""

    def setUp(self):
        self.district = DistrictFactory.create()
        self.county = CountyFactory.create()
        self.subcounty = SubCountyFactory.create()
        self.parish = ParishFactory.create()
        self.village = VillageFactory.create()

    # TODO TEST invalid payload
    # POST METHODS
    def test_register_farmer_created(self):
        url = reverse("register-farmer")
        data = {
          "firstName": "george",
          "lastName": "lucas",
          "identificationNumber": "242421212",
          "phoneNumber": "0788765234",
          "village": {
            "name": 'Some village',
            "id": self.village.id
          },
          "crops": ["beans", "maize", "sunflower","kales"]
        }
        response = client.post(url, data, format="json")

        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



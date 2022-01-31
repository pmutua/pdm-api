from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from pdm.apps.farmers.serializers import (
    FarmerDetailSerializer
)

from pdm.apps.authentication.factories import (
    UserFactory
)

from pdm.apps.demographics.tests.factories import (
    DistrictFactory,
    CountyFactory,
    SubCountyFactory,
    ParishFactory,
    VillageFactory
)

from pdm.apps.farmers.models import (
Crop,
Farmer,
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
        self.crop = Crop.objects.create(name="peas")
        self.user = UserFactory.create()
        self.farmer = Farmer.objects.create(
            user=self.user
        )

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
          "crops": [self.crop.id]
        }
        response = client.post(url, data, format="json")

        # self.assertEqual(response.data['success'], True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_a_crop_instance(self):
        url = reverse("crops")
        data = {"name": "Bananas"}
        res = client.post(url,data,format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_can_create_produce_record(self):
        url = reverse("add-produce")
        data = {
            "identification_no": self.user.identification_no,
            "crop": "managu",
            "produce_state": "sold",
            "value": 10000
        }
        res = client.post(url,data,format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)









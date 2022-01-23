from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from pdm.apps.authentication.models import (
    User,
    # Department
)

from pdm.apps.authentication.serializers import UserDetailSerializer
from .factories import UserFactory

# initialize the APIClient app
client = APIClient()


class PostAddNewUserTest(APITestCase):
    """Test module for POST add new user API"""

    def setUp(self):
        self.user = UserFactory

    def test_register_new_user(self):
        url = reverse("register_user")
        data = {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "roles": ["chief", "admin"],
            "phone": self.user.phone,
            "identification_no": self.user.identification_no,
            "department": "Ministry of Development",
        }
        response = client.post(url, data, format="json")
        user = User.objects.get(pk=response.json()["data"]["id"])
        serializer = UserDetailSerializer(user)
        self.assertEqual(response.data["data"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_post_invalid_user_payload(self):
    #     pass

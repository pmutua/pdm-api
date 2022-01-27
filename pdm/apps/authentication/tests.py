from django.urls import reverse
from django.contrib.auth.models import (
    Group,
)
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import faker
from .factories import (
    UserFactory,
)
from pdm.apps.authentication.models import (
    Department,
    User,
)
from pdm.apps.authentication.serializers import UserDetailSerializer


# initialize the APIClient app
client = APIClient()


class PostAddNewUserTest(APITestCase):
    """Test module for POST add new user API"""

    def setUp(self):
        self.user = UserFactory.create()
        self.department = Group.objects.create(name="Ministry of Developments")

    def test_register_new_user(self):
        url = reverse("register_user")
        data = {
            "first_name": "Steve",
            "last_name": "Yegon",
            "email": "steve@example.com",
            "roles": ["chief", "admin"],
            "phone": "25490345321",
            "identification_no": "535352222",
            "department": "Ministry of Urban Development",
        }
        response = client.post(url, data, format="json")
        user = User.objects.get(pk=response.json()["data"]["id"])
        serializer = UserDetailSerializer(user)
        self.assertEqual(response.data["data"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_user_already_registered(self):
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
        self.assertEqual(response.data["data"], None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostLoginUserTest(APITestCase):
    """Test module for POST add new user API"""

    def setUp(self):
        self.user = UserFactory.create()
        self.password = "899*&@#"
        self.user.set_password(self.password)
        self.department = Group.objects.create(name="Ministry of Developments")
        self.user.dept_id = self.department.id
        self.user.save()

        self.user.groups.add(self.department)
        pass

    def test_login_user(self):
        url = reverse("login")
        data = {
            "email": self.user.email,
            "password": self.password,
        }

        response = client.post(url, data, format="json")
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

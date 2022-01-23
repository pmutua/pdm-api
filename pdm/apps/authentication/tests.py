from django.test import TestCase,Client
from django.urls import reverse
from .models import (
User,
Department
)

# initialize the APIClient app
client = Client()


class PostAddNewUserTest(TestCase):
    """ Test module for GET single puppy API """

    def setUp(self):
        self.user = User.objects.create(
            first_name="Alice",
            last_name = "Williams",
            phone = '0722121111',
            dept_id = 1,
            identification_no = "26353244",
        )
        self.password = '354#162525'

        self.user.set_password(self.password)
        self.user.save()

        self.payload = {

        }

    def test_add_new_user(self):
        response = client.post(
            reverse('register_user',self.payload))

        print(response.json())

        # puppy = Puppy.objects.get(pk=self.rambo.pk)
        # serializer = PuppySerializer(puppy)
        # self.assertEqual(response.data, serializer.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_invalid_single_puppy(self):
    #     response = client.get(
    #         reverse('get_delete_update_puppy', kwargs={'pk': 30}))
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

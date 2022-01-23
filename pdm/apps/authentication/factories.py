# factories.py
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "authentication.User"

    username = "harun"
    password = "staffpassword"
    email = "harun@email.com"
    first_name = "Harun"
    last_name = "Daniels"
    dept_id = 1
    phone = "+254722345321"
    identification_no = "23453111"

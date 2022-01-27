from django.contrib.auth.models import (
    Group,
)
import factory
from factory import SubFactory
from factory.django import DjangoModelFactory
from pdm.apps.authentication.models import (
    Department,
    User
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('email')    # password = factory.LazyFunction(lambda: make_password('pi3.1415'))
    email = factory.Faker('email')
    first_name = factory.Faker('first_name', locale='es_ES')
    last_name = factory.Faker('last_name', locale='es_ES')
    phone = "+254722345321"
    identification_no = "23453111"



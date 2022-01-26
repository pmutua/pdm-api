
from factory import Faker
from factory.django import DjangoModelFactory
from ..models import District

fake = Faker()

class DistrictFactory(DjangoModelFactory):
    name = fake.city()

    class Meta:
        model = District

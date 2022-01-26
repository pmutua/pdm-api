
from factory import Faker
from factory.django import DjangoModelFactory
from ..models import District

class DistrictFactory(DjangoModelFactory):
    name = Faker('city')

    class Meta:
        model = District


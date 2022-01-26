
from factory import Faker
from factory.django import DjangoModelFactory
from  pdm.apps.demographics.models import District

class DistrictFactory(DjangoModelFactory):
    name = Faker('city')

    class Meta:
        model = District



from factory import (
    Faker,
    SubFactory
)
from factory.django import DjangoModelFactory
from  pdm.apps.demographics.models import (
    District,
    County,
    SubCounty,
    Parish,
    Village
)

class DistrictFactory(DjangoModelFactory):
    name = Faker('city')

    class Meta:
        model = District

class CountyFactory(DjangoModelFactory):
    name = Faker('city')
    district = SubFactory(DistrictFactory)

    class Meta:
        model = County

class SubCountyFactory(DjangoModelFactory):
    name = Faker('city')
    county = SubFactory(CountyFactory)

    class Meta:
        model = SubCounty

class ParishFactory(DjangoModelFactory):
    name = Faker('city')
    sub_county = SubFactory(SubCountyFactory)

    class Meta:
        model = Parish


class VillageFactory(DjangoModelFactory):
    name = Faker('city')
    parish = SubFactory(ParishFactory)

    class Meta:
        model = Village

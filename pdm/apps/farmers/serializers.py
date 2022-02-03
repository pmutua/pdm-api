from rest_framework import serializers
from pdm.apps.authentication.models import (
    User
)
from pdm.apps.demographics.serializers import VillageSerializer
from pdm.apps.farmers.models import (
    Crop,
    Farmer,
    Produce
)
from pdm.apps.demographics.models import (
    Village
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'identification_no']


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'


class FarmerCreateSerializer(serializers.Serializer):
    firstName = serializers.CharField(max_length=50)
    lastName = serializers.CharField(max_length=50)
    identificationNumber = serializers.CharField(max_length=50)
    phoneNumber = serializers.CharField(max_length=15)
    village = VillageSerializer()


class FarmerDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    village = VillageSerializer()
    crops = CropSerializer(many=True)

    class Meta:
        model = Farmer
        fields = '__all__'

class RecordProduceCreateSerializer(serializers.Serializer):
    """Validates incoming payload"""
    identification_no = serializers.CharField(max_length=50)
    produce_state =serializers.CharField(max_length=10)
    value = serializers.DecimalField(max_digits=12,decimal_places=2)
    crop = serializers.CharField(max_length=100)

class ProduceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = '__all__'

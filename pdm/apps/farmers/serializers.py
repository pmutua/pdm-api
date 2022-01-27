from rest_framework import serializers
from pdm.apps.authentication.models import (
    User
)
from pdm.apps.farmers.models import (
    Crop,
    Farmer
)
from pdm.apps.demographics.models import (
    Village
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'identification_no']


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ["id", 'name']


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

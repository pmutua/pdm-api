from rest_framework import serializers

from pdm.apps.farmers.serializers import FarmerDetailSerializer
from pdm.apps.production_storage_processing_marketing.models import *


class EvoucherSerializer(serializers.ModelSerializer):
    beneficiary = FarmerDetailSerializer()

    class Meta:
        model = Evoucher
        fields = '__all__'


class EvoucherCreateSerializer(serializers.Serializer):
    """Used to validate incoming payload. Only these fields are required when making request"""
    identification_no = serializers.CharField(max_length=50)
    farm_input = serializers.CharField(max_length=50)
    value = serializers.IntegerField()

class PSPMPillarPrograSerializer(serializers.Serializer):
    evouchers = EvoucherSerializer(many=True)
    class Meta:
        model = PillarProgram
        fields = '__all__'

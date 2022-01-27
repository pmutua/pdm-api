from rest_framework import serializers

from pdm.apps.farmers.serializers import FarmerDetailSerializer
from pdm.apps.production_storage_processing_marketing.models import *


class EvoucherSerializer(serializers.ModelSerializer):
    beneficiary = FarmerDetailSerializer()

    class Meta:
        model = Evoucher
        fields = '__all__'

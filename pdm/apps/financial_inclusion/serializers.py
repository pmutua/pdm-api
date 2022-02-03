from rest_framework import serializers

from pdm.apps.farmers.serializers import *
from pdm.apps.financial_inclusion.models import *


class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
        fields = "__all__"


class CommunityOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityOrganization
        fields = "__all__"


class InitiativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initiative
        fields = "__all__"


class BusinessDevelopmentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDevelopmentService
        fields = "__all__"


class SavingsSerializer(serializers.ModelSerializer):
    farmer = FarmerDetailSerializer()
    class Meta:
        model = Saving
        fields = "__all__"


class SavingsCreateSerializer(serializers.Serializer):
    """Used to validate incoming payload. Only these fields are required when making request"""
    identification_no = serializers.CharField(max_length=50)
    amount = serializers.FloatField()


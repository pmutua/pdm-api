from rest_framework import serializers

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

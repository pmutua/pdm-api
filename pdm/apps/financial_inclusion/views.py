from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from pdm.apps.financial_inclusion.models import *
from pdm.apps.financial_inclusion.serializers import *


class OrganizationTypeAPIView(ListCreateAPIView):
    serializer_class = OrganizationTypeSerializer
    queryset = OrganizationType.objects.all()


class CommunityOrganizationAPIView(ListCreateAPIView):
    serializer_class = CommunityOrganizationSerializer
    queryset = CommunityOrganization.objects.all()


class InitiativeAPIView(ListCreateAPIView):
    serializer_class = InitiativeSerializer
    queryset = Initiative.objects.all()


class BusinessDevelopmentServiceAPIView(ListCreateAPIView):
    serializer_class = BusinessDevelopmentServiceSerializer
    queryset = BusinessDevelopmentService.objects.all()

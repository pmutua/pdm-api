from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import DistrictSerializer, CountySerializer, SubCountySerializer, ParishSerializer, VillageSerializer
from .models import District, County, SubCounty, Parish, Village


class DistrictAPIView(ListCreateAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class DistrictDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class CountyAPIView(ListCreateAPIView):
    serializer_class = CountySerializer
    queryset = County.objects.all()


class CountyDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CountySerializer
    queryset = County.objects.all()


class SubCountyAPIView(ListCreateAPIView):
    serializer_class = SubCountySerializer
    queryset = SubCounty.objects.all()


class SubCountyDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubCountySerializer
    queryset = SubCounty.objects.all()


class ParishAPIView(ListCreateAPIView):
    serializer_class = ParishSerializer
    queryset = Parish.objects.all()


class ParishDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParishSerializer
    queryset = Parish.objects.all()


class VillageAPIView(ListCreateAPIView):
    serializer_class = VillageSerializer
    queryset = Village.objects.all()


class VillageDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = VillageSerializer
    queryset = Village.objects.all()

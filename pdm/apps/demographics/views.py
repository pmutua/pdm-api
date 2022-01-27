from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DistrictSerializer, CountySerializer, SubCountySerializer, ParishSerializer, VillageSerializer
from .models import District, County, SubCounty, Parish, Village
from ..financial_inclusion.models import BusinessDevelopmentService


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


class DistrictSpendingAPIView(APIView):
    def get(self, request):
        res = {}
        districts = District.objects.all()
        spending_analysis = []
        for district in districts:
            counties = County.objects.filter(district__id=district.id)
            for county in counties:
                sub_counties = SubCounty.objects.filter(county__id=county.id)
                for sub_county in sub_counties:
                    parishes = Parish.objects.filter(sub_county__id=sub_county.id)
                    for parish in parishes:
                        villages = Village.objects.filter(parish__id=parish.id)
                        for village in villages:
                            business_evelopment_services = BusinessDevelopmentService.objects.filter(
                                village__id=village.id)
                            budget_spend = 0
                            for business_evelopment_service in business_evelopment_services:
                                budget_spend += business_evelopment_service.budget_spend
                            district_spending_analysis = {}
                            district_spending_analysis["district"] = district.name
                            district_spending_analysis["budget_spend"] = budget_spend
                            spending_analysis.append(district_spending_analysis)
        res["data"] = spending_analysis
        res["success"] = True

        return Response(res)

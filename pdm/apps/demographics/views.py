from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DistrictSerializer, CountySerializer, SubCountySerializer, ParishSerializer, VillageSerializer
from .models import District, County, SubCounty, Parish, Village
from ..financial_inclusion.models import BusinessDevelopmentService
from ..financial_inclusion.serializers import BusinessDevelopmentServiceSerializer


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


class ParishDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParishSerializer
    queryset = Parish.objects.all()


class VillageAPIView(ListCreateAPIView):
    serializer_class = VillageSerializer
    queryset = Village.objects.all()

class ParishAPIView(APIView):
    def post(self, request):
        request_data = request.data
        name = request_data['name'],
        sub_county_id = request_data['sub_county']
        sub_county = SubCounty.objects.get(id=sub_county_id)

        obj, created = Parish.objects.get_or_create(
            name=name,
            sub_county = sub_county
        )
        if created:
            message = "Parish created"
        else:
            message = "Error creating Parish"
        res = {"message": message}

        return Response(res)

    def get(self, request):
        parish = Parish.objects.all()
        parish_serializer = ParishSerializer(parish, many=True)
        res = {"data": parish_serializer.data}
        return Response(res)

class VillageDetailAPIView(APIView):
    def post(self, request):
        request_data = request.data
        name = request_data['name'],
        parish_id = request_data['parish']
        parish = Parish.objects.get(id=parish_id)

        obj, created = Village.objects.get_or_create(
            name=name,
            parish = parish
        )
        if created:
            message = "Village created"
        else:
            message = "Error creating village"
        res = {"message": message}

        return Response(res)

    def get(self, request):
        Villages = Village.objects.all()
        village_serializer = VillageSerializer(Villages, many=True)
        res = {"data": village_serializer.data}
        return Response(res)

class DistrictSpendingAPIView(APIView):
    def get(self, request):
        districts = District.objects.all()
        district_totals = []
        for district in districts:
            district_serializer = DistrictSerializer(district)
            counties = County.objects.filter(district_id=district.id)
            subcounties = SubCounty.objects.filter(county_id__in=counties)
            parishes = Parish.objects.filter(sub_county_id__in=subcounties)
            villages = Village.objects.filter(parish_id__in=parishes)
            business_development_services = BusinessDevelopmentService.objects.filter(village_id__in=villages)

            district_budget_spend = business_development_services.aggregate(Sum("budget_spend")).get(
                "budget_spend__sum") if business_development_services else 0
            district_totals.append(
                {"district": district_serializer.data, "district_budget_spend": district_budget_spend})

        res = {"data": district_totals}
        return Response(res, status=status.HTTP_200_OK)

    def post(self, request):
        res = {"message": "OK"}
        return Response(res, status=status.HTTP_200_OK)


class ParishDashboardAPIView(APIView):
    def get(self, request):
        parish_id = request.GET.get("parish")
        if parish_id:
            parish = None
            try:
                parish = Parish.objects.get(id=parish_id)
            except ObjectDoesNotExist:
                res = {"data": None, "message": "Provide valid parish"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            res = {"id": parish.id, "name": parish.name, "subcounty": parish.sub_county.name,
                   "county": parish.sub_county.county.name, "district": parish.sub_county.county.district.name}

            business_development_services = BusinessDevelopmentService.objects.filter(village__parish__id=parish_id)
            business_development_services_serializer = BusinessDevelopmentServiceSerializer(business_development_services, many=True)
            res["business_development_services_budget_spend"] = business_development_services.aggregate(Sum("budget_spend"))["budget_spend__sum"] or 0
            res["business_development_services"] = business_development_services_serializer.data
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {"data": None, "message": "Provide parish"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        res = {"message": "OK"}
        return Response(res, status=status.HTTP_200_OK)

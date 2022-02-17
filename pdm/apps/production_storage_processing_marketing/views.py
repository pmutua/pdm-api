import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from pdm.apps.farmers.models import (
    Farmer,
    Produce
)
from pdm.apps.demographics.models import *
from pdm.apps.production_storage_processing_marketing.models import *
from pdm.apps.production_storage_processing_marketing.serializers import *

from .utilities import autogenerate_evoucher_no, DecimalEncoder
from ..demographics.serializers import *


class EvouchersAPIView(ListCreateAPIView):
    serializer_class = EvoucherSerializer
    queryset = Evoucher.objects.all()

    def post(self, request):
        req = request.data
        serializer = EvoucherCreateSerializer(data=req)
        res = {}
        national_id = req.get("identification_no")
        try:
            farmer = Farmer.objects.get(user__identification_no=national_id)
            if serializer.is_valid():
                value = req.get("value")
                farm_input = req.get("farm_input")

                evoucher = Evoucher.objects.create(beneficiary=farmer, value=value, farm_input=farm_input)
                evoucher.voucher_no = autogenerate_evoucher_no()
                evoucher.save()
                evoucher_serializer = EvoucherSerializer(evoucher)
                res["msg"] = "E-voucher successfully created"
                res["success"] = True
                res["data"] = evoucher_serializer.data
                return Response(res, status=status.HTTP_201_CREATED)
            res = {"success": False, "msg": serializer.errors, "data": None}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = {"success": False, "msg": str(e), "data": None}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class DashBoardApiView(ListCreateAPIView):
    serializer_class = PSPMPillarPrograSerializer
    queryset = PSPMPillarProgram.objects.all()

    def get(self, request):
        districts_data = {
            "total_evouchers_issued": Evoucher.objects.all().aggregate(Sum("value"))["value__sum"] or 0,
            "no_of_farmers_registered": Farmer.objects.all().count(),
            "total_income_value_from_processing":
                Produce.objects.filter(produce_in__iexact='sold').aggregate(Sum("value"))["value__sum"] or 0,
            "total_value_of_produce_in_storage":
                Produce.objects.filter(produce_in__iexact='storage').aggregate(Sum("value"))["value__sum"] or 0,
            "districts": [
                {
                    "id": district.id,
                    "name": district.name,
                    "counties": [
                        {
                            "id": county.id,
                            "name": county.name,
                            "sub_counties": [
                                {
                                    "id": subcounty.id,
                                    "name": subcounty.name,
                                    "parishes": [
                                        {
                                            "id": parish.id,
                                            "name": parish.name,
                                            "villages": [
                                                {
                                                    "id": village.id,
                                                    "name": village.name,
                                                    "total": Evoucher.objects.filter(
                                                        beneficiary__village__id=village.id
                                                    ).aggregate(Sum("value"))["value__sum"]
                                                             or 0,
                                                    "income_processing_value": Produce.objects.filter(
                                                        produce_in__iexact='sold',
                                                        owner__village__id=village.id
                                                    ).aggregate(Sum("value"))["value__sum"]
                                                                               or 0,
                                                    "total_value_of_produce_in_storage":
                                                        Produce.objects.filter(produce_in__iexact='storage',
                                                                               owner__village__id=village.id).aggregate(
                                                            Sum("value"))[
                                                            "value__sum"] or 0,
                                                }
                                                for village in parish.villages.all()
                                            ],
                                            "total": Evoucher.objects.filter(
                                                beneficiary__village__parish__id=parish.id
                                            ).aggregate(Sum("value"))["value__sum"]
                                                     or 0,
                                            "income_processing_value": Produce.objects.filter(
                                                produce_in__iexact='sold',
                                                owner__village__parish__id=parish.id
                                            ).aggregate(Sum("value"))["value__sum"]
                                                                       or 0,
                                            "total_value_of_produce_in_storage":
                                                Produce.objects.filter(produce_in__iexact='storage',
                                                                       owner__village__parish__id=parish.id).aggregate(
                                                    Sum("value"))[
                                                    "value__sum"] or 0,
                                        }
                                        for parish in subcounty.parishes.all()
                                    ],
                                    "total": Evoucher.objects.filter(
                                        beneficiary__village__parish__sub_county__id=subcounty.id
                                    ).aggregate(Sum("value"))["value__sum"]
                                             or 0,
                                    "income_processing_value": Produce.objects.filter(
                                        produce_in__iexact='sold',
                                        owner__village__parish__sub_county__id=subcounty.id
                                    ).aggregate(Sum("value"))["value__sum"]
                                                               or 0,
                                    "total_value_of_produce_in_storage":
                                        Produce.objects.filter(produce_in__iexact='storage',
                                                               owner__village__parish__sub_county__id=subcounty.id).aggregate(
                                            Sum("value"))[
                                            "value__sum"] or 0,
                                }
                                for subcounty in county.sub_counties.all()
                            ],
                            "total": Evoucher.objects.filter(
                                beneficiary__village__parish__sub_county__county__id=county.id
                            ).aggregate(Sum("value"))["value__sum"]
                                     or 0,
                            "income_processing_value": Produce.objects.filter(
                                produce_in__iexact='sold',
                                owner__village__parish__sub_county__county__id=county.id
                            ).aggregate(Sum("value"))["value__sum"]
                                                       or 0,
                            "total_value_of_produce_in_storage":
                                Produce.objects.filter(produce_in__iexact='storage',
                                                       owner__village__parish__sub_county__county__id=county.id).aggregate(
                                    Sum("value"))[
                                    "value__sum"] or 0,
                        }
                        for county in district.counties.all()
                    ],
                    "total": Evoucher.objects.filter(
                        beneficiary__village__parish__sub_county__county__district__id=district.id
                    ).aggregate(Sum("value"))["value__sum"]
                             or 0,
                    "income_processing_value": Produce.objects.filter(
                        produce_in__iexact='sold',
                        owner__village__parish__sub_county__county__district__id=district.id
                    ).aggregate(Sum("value"))["value__sum"]
                                               or 0,
                    "total_value_of_produce_in_storage":
                        Produce.objects.filter(produce_in__iexact='storage',
                                               owner__village__parish__sub_county__county__district__id=district.id).aggregate(
                            Sum("value"))[
                            "value__sum"] or 0,
                    "total_farmers_registered":
                        Farmer.objects.filter(village__parish__sub_county__county__district__id=district.id).count(),
                }
                for district in District.objects.all()
            ],
        }
        return Response(data=json.dumps(districts_data, cls=DecimalEncoder))


class SetUpPillarAPIView(APIView):
    def post(self, request):
        data = request.data
        commencement_date = data.get('date')
        funds_disbursed = data.get('funds_disbursed')
        obj = PSPMPillarProgram.objects.create(
            commencement_date=commencement_date,
            funds_disbursed=funds_disbursed
        )


# evouchers summary per cunty, subcounty and the likes

class EvouchersSummariesView(APIView):
    def post(self, request):
        res = {"message": "OK"}
        return Response(res, status=status.HTTP_200_OK)

    def get(self, request):
        district_id = request.GET.get("district")
        county_id = request.GET.get("county")
        subcounty_id = request.GET.get("subcounty")
        parish_id = request.GET.get("parish")

        if district_id:
            district = None
            try:
                district = District.objects.get(id=district_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid district id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            counties = County.objects.filter(district_id=district_id)
            total_evouchers_count = 0
            county_evouchers = []
            for county in counties:
                sub_counties = SubCounty.objects.filter(county_id__in=counties)
                parishes = Parish.objects.filter(sub_county_id__in=sub_counties)
                villages = Village.objects.filter(parish_id__in=parishes)
                beneficiaries = Farmer.objects.filter(village_id__in=villages)
                evoucher_count = Evoucher.objects.filter(beneficiary_id__in=beneficiaries).count()
                county_serializer = CountySerializer(county)
                county_details = county_serializer.data
                county_details["evouchers"] = evoucher_count
                county_evouchers.append(county_details)
                total_evouchers_count += evoucher_count
            district_serializer = DistrictSerializer(district)
            res = {"total_evoucher": total_evouchers_count, "district": district_serializer.data,
                   "counties": county_evouchers}
            return Response(res, status=status.HTTP_200_OK)
        if county_id:
            county = None
            try:
                county = County.objects.get(id=county_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid county id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            sub_counties = SubCounty.objects.filter(county_id=county_id)
            total_evouchers_count = 0
            sub_county_evouchers = []
            for sub_county in sub_counties:
                parishes = Parish.objects.filter(sub_county_id__in=sub_counties)
                villages = Village.objects.filter(parish_id__in=parishes)
                beneficiaries = Farmer.objects.filter(village_id__in=villages)
                evoucher_count = Evoucher.objects.filter(beneficiary_id__in=beneficiaries).count()
                sub_county_serializer = SubCountySerializer(sub_county)
                sub_county_details = sub_county_serializer.data
                sub_county_details["evouchers"] = evoucher_count
                sub_county_evouchers.append(sub_county_details)
                total_evouchers_count += evoucher_count
            county_serializer = CountySerializer(county)
            res = {"total_evouchers": total_evouchers_count, "county": county_serializer.data,
                   "sub_counties": sub_county_evouchers}
            return Response(res, status=status.HTTP_200_OK)
        if subcounty_id:
            subcounty = None
            try:
                subcounty = SubCounty.objects.get(id=subcounty_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid subcounty id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            parishes = Parish.objects.filter(sub_county_id=subcounty_id)
            total_evouchers_count = 0
            parish_evouchers = []
            for parish in parishes:
                villages = Village.objects.filter(parish_id__in=parishes)
                beneficiaries = Farmer.objects.filter(village_id__in=villages)
                evoucher_count = Evoucher.objects.filter(beneficiary_id__in=beneficiaries).count()
                parish_serializer = ParishSerializer(parish)
                parish_details = parish_serializer.data
                parish_details["evouchers"] = evoucher_count
                parish_evouchers.append(parish_details)
                total_evouchers_count += evoucher_count
            subcounty_serializer = SubCountySerializer(subcounty)
            res = {"total_evouchers": total_evouchers_count, "subcounty": subcounty_serializer.data,
                   "parishes": parish_evouchers}
            return Response(res, status=status.HTTP_200_OK)
        if parish_id:
            parish = None
            try:
                parish = Parish.objects.get(id=parish_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid parish id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            villages = Village.objects.filter(parish_id=parish_id)
            total_evouchers_count = 0
            village_evouchers = []
            for village in villages:
                beneficiaries = Farmer.objects.filter(village_id__in=villages)
                evoucher_count = Evoucher.objects.filter(beneficiary_id__in=beneficiaries).count()
                village_serializer = VillageSerializer(village)
                village_details = village_serializer.data
                village_details["evouchers"] = evoucher_count
                village_evouchers.append(village_details)
                total_evouchers_count += evoucher_count
            parish_serializer = ParishSerializer(parish)
            res = {"total_evouchers": total_evouchers_count,
                   "villages": village_evouchers}
            return Response(res, status=status.HTTP_200_OK)
        else:
            evoucher_count = Evoucher.objects.all().count()
            res = {"total_evouchers": evoucher_count}
            return Response(res, status=status.HTTP_200_OK)

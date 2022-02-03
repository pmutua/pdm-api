import json
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from pdm.apps.farmers.models import (
    Farmer,
    Produce
)
from pdm.apps.demographics.models import District, County
from pdm.apps.production_storage_processing_marketing.models import (
    Evoucher,
    PSPMPillarProgram
)
from pdm.apps.production_storage_processing_marketing.serializers import (
    EvoucherSerializer,
    EvoucherCreateSerializer,
    PSPMPillarPrograSerializer,
)

from .utilities import autogenerate_evoucher_no, DecimalEncoder


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
            "total_income_value_from_processing": Produce.objects.filter(produce_in__iexact='sold').aggregate(Sum("value"))["value__sum"] or 0,
            "total_value_of_produce_in_storage": Produce.objects.filter(produce_in__iexact='storage').aggregate(Sum("value"))["value__sum"] or 0,
            "districts": [
                {
                    "id":district.id,
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
                                Produce.objects.filter(produce_in__iexact='storage',owner__village__parish__sub_county__county__id=county.id).aggregate(Sum("value"))[
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
    def post(self,request):
        data = request.data
        commencement_date = data.get('date')
        funds_disbursed = data.get('funds_disbursed')
        obj = PSPMPillarProgram.objects.create(
            commencement_date=commencement_date,
            funds_disbursed=funds_disbursed
        )



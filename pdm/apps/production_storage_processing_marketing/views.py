from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
ListCreateAPIView
)

from pdm.apps.farmers.models import Farmer
from pdm.apps.production_storage_processing_marketing.models import Evoucher
from pdm.apps.production_storage_processing_marketing.serializers import (
    EvoucherSerializer,
    EvoucherCreateSerializer
)

from .utilities import autogenerate_evoucher_no


class EvouchersAPIView(ListCreateAPIView):
    serializer_class = EvoucherSerializer
    queryset = Evoucher.objects.all()

    def post(self, request):
        req = request.data
        serializer = EvoucherCreateSerializer(data=req)
        res ={}
        national_id = req.get("identification_no")
        try:
            farmer = Farmer.objects.get(user__identification_no=national_id)
            if serializer.is_valid():
                value = req.get("value")
                farm_input = req.get("farm_input")

                evoucher = Evoucher.objects.create(beneficiary=farmer,
                                                   value=value,
                                                   farm_input=farm_input)
                evoucher.voucher_no = autogenerate_evoucher_no()
                evoucher.save()
                evoucher_serializer = EvoucherSerializer(evoucher)
                res['msg'] = "E-voucher successfully created"
                res['success'] = True
                res['data'] = evoucher_serializer.data
                return Response(res,status=status.HTTP_201_CREATED)
            res = {"success": True, "msg": serializer.errors, "data":None}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = {"success": True, "msg": str(e), "data":None}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)






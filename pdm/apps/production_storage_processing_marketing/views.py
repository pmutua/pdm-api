from rest_framework.response import Response
from rest_framework.views import APIView

from pdm.apps.farmers.models import Farmer
from pdm.apps.production_storage_processing_marketing.models import Evoucher
from pdm.apps.production_storage_processing_marketing.serializers import EvoucherSerializer


class EvouchersAPIView(APIView):
    def get(self, request):
        evouchers = Evoucher.objects.all()
        evouchers_serializer = EvoucherSerializer(evouchers, many=True)
        res = {}
        res["data"] = evouchers_serializer.data
        res["success"] = True

        return Response(res)

    def post(self, request):
        request_data = request.data
        beneficiary = request_data.get("beneficiary")
        voucher_no = request_data.get("voucher_no")
        value = request_data.get("value")
        farm_input = request_data.get("farm_input")
        farmer = Farmer.objects.get(id=beneficiary)
        evoucher = Evoucher.objects.create(beneficiary=farmer,
                                           voucher_no=voucher_no,
                                           value=value,
                                           farm_input=farm_input)
        evouchers_serializer = EvoucherSerializer(evoucher)

        res = {"success": True, "evoucher": evouchers_serializer.data}
        return Response(res)

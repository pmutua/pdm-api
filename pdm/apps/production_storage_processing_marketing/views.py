from rest_framework.generics import ListCreateAPIView

from pdm.apps.production_storage_processing_marketing.models import Evoucher
from pdm.apps.production_storage_processing_marketing.serializers import EvoucherSerializer


class EvouchersAPIView(ListCreateAPIView):
    serializer_class = EvoucherSerializer
    queryset = Evoucher.objects.all()

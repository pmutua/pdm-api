from rest_framework.generics import (
ListCreateAPIView
)
from rest_framework import status
from rest_framework.response import  Response

from .serializers import DistrictSerializer
from .models import (
District
)

class DistrictAPIView(ListCreateAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()

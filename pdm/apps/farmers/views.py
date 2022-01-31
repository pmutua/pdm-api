from django.contrib.auth.models import (
    Group,
)
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pdm.apps.farmers.models import Crop, Farmer
from pdm.apps.authentication.models import User
from pdm.apps.farmers.serializers import (
    FarmerCreateSerializer,
    FarmerDetailSerializer,
    CropSerializer
)

from pdm.apps.demographics.models import Village


class RegisterFarmerAPIView(APIView):
    def post(self, request):
        req = request.data
        serializer = FarmerCreateSerializer(data=req)

        if serializer.is_valid():
            try:
                village = Village.objects.get(id=req["village"]["id"])
                group, _ = Group.objects.get_or_create(name="Farmer")
                user = User.objects.create(
                    first_name=req.get("firstName"),
                    last_name=req.get("lastName"),
                    username=req.get("identificationNumber"),
                    phone=req.get("phoneNumber"),
                    identification_no=req.get("identificationNumber"),
                )
                user.groups.add(group)

                farmer = Farmer.objects.create(user=user)
                farmer.village = village
                farmer.save()
                for crop_id in req.get("crops"):
                    c = Crop.objects.filter(id=crop_id)[0]
                    farmer.crops.add(c)

                ser = FarmerDetailSerializer(farmer)

                res = {"success": True,"msg": "Farmer success fully created", "data": ser.data, "status": status.HTTP_201_CREATED}
                return Response(data=res, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(str(e))
                res = {"success": False, "msg": str(e), "data": None}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

        res = {"success": False, "msg": str(serializer.errors), "data": None}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class FarmersAPIView(ListCreateAPIView):
    serializer_class = FarmerDetailSerializer
    queryset = Farmer.objects.all()


class CropAPIView(ListCreateAPIView):
    serializer_class = CropSerializer
    queryset = Crop.objects.all()



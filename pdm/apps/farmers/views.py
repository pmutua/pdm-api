from django.contrib.auth.models import (
    Group,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pdm.apps.farmers.models import Crop, Farmer
from pdm.apps.authentication.models import User
from pdm.apps.farmers.serializers import FarmerCreateSerializer, FarmerDetailSerializer

from pdm.apps.demographics.models import Village


class RegisterFarmerAPIView(APIView):
    def post(self, request):
        """
        {
          "firstName": "george",
          "lastName": "lucas",
          "identificationNumber": "242421212",
          "phoneNumber": "0788765234",
          "village": {
            "name": "LUCON",
            "id": 2
          },
          "crops": ["beans", "maize", "sunflower","kales"]
        }
        """
        req = request.data
        serializer = FarmerCreateSerializer(data=req)

        if serializer.is_valid():
            try:
                village = Village.objects.get(id=req["village"]["id"])
                group, _ = Group.objects.get_or_create(name="Farmer")
                user = User.objects.create(
                    first_name=req.get("firstName"),
                    last_name=req.get("lastName"),
                    phone=req.get("phoneNumber"),
                    identification_no=req.get("identificationNumber"),
                )
                user.groups.add(group)

                farmer = Farmer.objects.create(user=user, village=village)
                for crop in req.get("crops"):
                    c, _ = Crop.objects.get_or_create(name=crop)
                    farmer.crops.add(c)

                ser = FarmerDetailSerializer(farmer)

                res = {"success": True, "data": ser.data, "status": status.HTTP_201_CREATED}
                return Response(data=res, status=status.HTTP_201_CREATED)

            except Exception as e:
                res = {"success": False, "msg": str(e), "data": None}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

        res = {"success": False, "msg": str(serializer.errors), "data": None}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

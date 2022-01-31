from django.contrib.auth.models import (
    Group,
)
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pdm.apps.farmers.models import (
    Crop,
    Farmer,
    Produce
)
from pdm.apps.authentication.models import User
from pdm.apps.farmers.serializers import (
    FarmerCreateSerializer,
    FarmerDetailSerializer,
    CropSerializer,
    RecordProduceCreateSerializer,
    ProduceDetailSerializer
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

                res = {"success": True,"msg": "Farmer successfully created", "data": ser.data, "status": status.HTTP_201_CREATED}
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

class RecordProduceAPIview(APIView):
    def post(self,request):
        print(request.data)

        try:
            serializers = RecordProduceCreateSerializer(data=request.data)
            if serializers.is_valid():
                farmer_identification_no = request.data.get('identification_no')
                produce_state = request.data.get('produce_state')
                value = request.data.get('value')
                farmer = Farmer.objects.get(user__identification_no=farmer_identification_no)
                crop,_ = Crop.objects.get_or_create(name=request.data.get('crop'))

                obj = Produce(
                    owner= farmer,
                    crop = crop,
                    produce_in = produce_state,
                    value = value
                )
                obj.save()
                ser = ProduceDetailSerializer(obj)
                res = {"success": True,"msg": "Produce details successfully created!", "data": ser.data, "status": status.HTTP_201_CREATED}
                return Response(data=res, status=status.HTTP_201_CREATED)
            res = {"success": False, "msg": serializers.errors, "data": None}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            res = {"success": False, "msg": str(e), "data": None}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class ProduceDataAPIView(APIView):
    def get(self,request):
        all_produce_count = Produce.objects.all().count()
        produce_in_market = Produce.objects.filter(produce_in='markets').count()
        produce_sold = Produce.objects.filter(produce_in='sold').count()
        produce_in_storage = Produce.objects.filter(produce_in='storage').count()

        markets_percentage = 0 if all_produce_count == 0 else (produce_in_market/all_produce_count)*100
        sold_percentage = 0 if all_produce_count == 0 else (produce_sold/all_produce_count) *100
        storage_percentage  = 0 if all_produce_count == 0 else  (produce_in_storage/all_produce_count) *100
        data = {
            "markets": {
                "percentage": markets_percentage,
                "data": [[crop.name,
                          (0 if produce_in_storage == 0 else Produce.objects.filter(produce_in='sold', crop__id=crop.id).count() / produce_in_market) * 100]
                         for crop in Crop.objects.all().distinct()
                         ],
            },
            "sold": {
                "percentage": sold_percentage,
                "data": [ [crop.name,(Produce.objects.filter(produce_in='sold', crop__id=crop.id).count()/produce_sold)*100]
                          for crop in Crop.objects.all().distinct()
                          ],
            },
            "storage":{
                "percentage": storage_percentage,
                "data": [ [crop.name,(0 if produce_in_storage == 0 else Produce.objects.filter(produce_in='storage', crop__id=crop.id).count()/produce_in_storage)*100]
                          for crop in Crop.objects.all().distinct()
                          ],
            },
            "produce_distribution": [
                    {
                        "name":crop.name,
                        "y": (0 if all_produce_count == 0 else Produce.objects.filter(crop__id=crop.id).count() / all_produce_count) * 100}
                         for crop in Crop.objects.all().distinct()
                         ],

        }

        return Response(data)



class ProduceDataFilterByDistrictAPIView(APIView):
    def get(self,request):
        _id  = self.request.GET.get('q')
        all_produce_count = Produce.objects.filter(owner__village__parish__sub_county__county__district__id=_id).count()
        produce_in_market = Produce.objects.filter(produce_in='markets',owner__village__parish__sub_county__county__district__id=_id).count()
        produce_sold = Produce.objects.filter(produce_in='sold',owner__village__parish__sub_county__county__district__id=_id).count()
        produce_in_storage = Produce.objects.filter(produce_in='storage',owner__village__parish__sub_county__county__district__id=_id).count()

        markets_percentage = 0 if all_produce_count == 0 else (produce_in_market/all_produce_count)*100
        sold_percentage = 0 if all_produce_count == 0 else (produce_sold/all_produce_count) *100
        storage_percentage  = 0 if all_produce_count == 0 else  (produce_in_storage/all_produce_count) *100
        data = {
            "markets": {
                "percentage": markets_percentage,
                "data": [[crop.name,
                          (0 if produce_in_storage == 0 else Produce.objects.filter(produce_in='sold', crop__id=crop.id,owner__village__parish__sub_county__county__district__id=_id).count() / produce_in_market) * 100]
                         for crop in Crop.objects.all().distinct()
                         ],
            },
            "sold": {
                "percentage": sold_percentage,
                "data": [ [crop.name,(Produce.objects.filter(produce_in='sold', crop__id=crop.id,owner__village__parish__sub_county__county__district__id=_id).count()/produce_sold)*100]
                          for crop in Crop.objects.all().distinct()
                          ],
            },
            "storage":{
                "percentage": storage_percentage,
                "data": [ [crop.name,(0 if produce_in_storage == 0 else Produce.objects.filter(produce_in='storage', crop__id=crop.id,owner__village__parish__sub_county__county__district__id=_id).count()/produce_in_storage)*100]
                          for crop in Crop.objects.all().distinct()
                          ],
            },
            "produce_distribution": [
                    {
                        "name":crop.name,
                        "y": (0 if all_produce_count == 0 else Produce.objects.filter(crop__id=crop.id,owner__village__parish__sub_county__county__district__id=_id).count() / all_produce_count) * 100}
                         for crop in Crop.objects.all().distinct()
                         ],

        }

        return Response(data)



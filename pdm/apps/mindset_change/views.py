from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pdm.apps.mindset_change.models import *
from pdm.apps.mindset_change.serializers import *


# Create your views here.

class MindSetChampionView(APIView):
    def post(self, request):
        request_data = request.data
        serializer = MindSetChampionSerilaizer(data=request_data)
        if serializer.is_valid():
            name = request_data['name']
            phone = request_data['phone']
            email = request_data['email']
            district_id = int(request_data['district'])
            district = None
            try:
                district = District.objects.get(id=district_id)
            except ObjectDoesNotExist:
                res = {"success": False, "msg": "Provide valid district id", "data": None}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            mind_set_champion = MindSetChampion.objects.create(name=name, phone=phone, email=email, district=district)
            mind_set_champions_serializer = MindSetChampionSerilaizer(mind_set_champion)
            res = {"message": "MindSetChampion added", "data": mind_set_champions_serializer.data}
            return Response(res)
        else:
            res = {"success": False, "msg": serializer.errors, "data": None}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        district_id = request.GET.get("district")
        if district_id:
            mind_set_champions = MindSetChampion.objects.filter(district__id=district_id)
            mind_set_champions_serializer = MindSetChampionSerilaizer(mind_set_champions, many=True)
            res = {"data": mind_set_champions_serializer.data}
            return Response(res, status=status.HTTP_200_OK)
        else:
            mind_set_champions = MindSetChampion.objects.all()
            mind_set_champions_serializer = MindSetChampionSerilaizer(mind_set_champions, many=True)
            res = {"data": mind_set_champions_serializer.data}
            return Response(res, status=status.HTTP_200_OK)

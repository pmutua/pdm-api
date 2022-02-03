from rest_framework import serializers

from pdm.apps.mindset_change.models import *
from .models import *
from ..demographics.serializers import DistrictSerializer


class MindSetChampionSerilaizer(serializers.ModelSerializer):
    district = DistrictSerializer()
    class Meta:
        model = MindSetChampion
        fields = "__all__"

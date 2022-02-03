from rest_framework import serializers
from pdm.apps.demographics.models import District, County, SubCounty, Parish, Village


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = "__all__"


class SubCountySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCounty
        fields = "__all__"


class ParishSerializer(serializers.ModelSerializer):
    sub_county = SubCountySerializer()
    class Meta:
        model = Parish
        fields = "__all__"


class VillageSerializer(serializers.ModelSerializer):
    parish = ParishSerializer()
    class Meta:
        model = Village
        fields = "__all__"

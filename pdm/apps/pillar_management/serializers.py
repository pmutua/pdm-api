from rest_framework import serializers

from pdm.apps.demographics.serializers import *
from pdm.apps.pillar_management.models import *


class PublicSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicSector
        fields = "__all__"


class PillarProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = PillarProgram
        fields = "__all__"


class PillarProgramDisbursementSerializer(serializers.ModelSerializer):
    pillar_program = PillarProgramSerializer()

    class Meta:
        model = PillarProgramDisbursement
        fields = "__all__"


class SectorDisbursementSerializer(serializers.ModelSerializer):
    pillar_program = PillarProgramSerializer()
    public_sector = PublicSectorSerializer()

    class Meta:
        model = PublicSectorDisbursement
        fields = "__all__"


class DistrictDisbursementSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()
    pillar_program = PillarProgramSerializer()
    public_sector = PublicSectorSerializer()

    class Meta:
        model = DistrictDisbursement
        fields = "__all__"


class CountyDisbursementSerializer(serializers.ModelSerializer):
    county = CountySerializer()
    pillar_program = PillarProgramSerializer()
    public_sector = PublicSectorSerializer()

    class Meta:
        model = CountyDisbursement
        fields = "__all__"


class SubCountyDisbursementSerializer(serializers.ModelSerializer):
    subcounty = SubCountySerializer()
    pillar_program = PillarProgramSerializer()
    public_sector = PublicSectorSerializer()

    class Meta:
        model = SubCountyDisbursement
        fields = "__all__"


class ParishDisbursementSerializer(serializers.ModelSerializer):
    parish = ParishSerializer()
    pillar_program = PillarProgramSerializer()
    public_sector = PublicSectorSerializer()

    class Meta:
        model = ParishDisbursement
        fields = "__all__"


class VillageDisbursementSerializer(serializers.ModelSerializer):
    village = VillageSerializer()
    pillar_program = PillarProgramSerializer()
    public_sector = PublicSectorSerializer()

    class Meta:
        model = VillageDisbursement
        fields = "__all__"

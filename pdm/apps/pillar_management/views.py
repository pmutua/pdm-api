from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from pdm.apps.demographics.models import *
from pdm.apps.demographics.serializers import *
from pdm.apps.pillar_management.serializers import *
from pdm.apps.pillar_management.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum


class PublicSectorAPIView(APIView):
    def post(self, request):
        request_data = request.data
        name = request_data["name"]
        code = request_data["code"]

        obj, created = PublicSector.objects.get_or_create(
            name=name,
            code=code,
        )
        if created:
            message = "Public sector created successfully"
        else:
            message = "Error creating public sector"
        res = {"message": message}

        return Response(res)

    def get(self, request):
        public_sectors = PublicSector.objects.all()
        public_sector_serializers = PublicSectorSerializer(public_sectors, many=True)
        res = {"data": public_sector_serializers.data}
        return Response(res)


class PillarProgramAPIView(APIView):
    def post(self, request):
        request_data = request.data
        name = request_data["name"]
        description = request_data["description"]
        start_year = request_data["start_year"]

        obj, created = PillarProgram.objects.get_or_create(
            name=name,
            description=description,
            start_year=start_year,
        )
        if created:
            message = "Pillar program created"
        else:
            message = "Error creating pillar program"
        res = {"message": message}

        return Response(res)

    def get(self, request):
        pillar_programs = PillarProgram.objects.all()
        pillar_program_serializer = PillarProgramSerializer(pillar_programs, many=True)
        res = {"data": pillar_program_serializer.data}
        return Response(res)


# get funds disbursed per county, district, subcounty, parish


class PillarProgramDisbursementAPIView(APIView):
    def post(self, request):
        request_data = request.data
        amount = request_data["amount"]
        pillar_program_id = request_data["pillar_program"]

        pillar_program = None
        try:
            pillar_program = PillarProgram.objects.get(id=pillar_program_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid pillar_program id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        disbursement = PillarProgramDisbursement.objects.create(amount=amount, pillar_program=pillar_program)
        disbursement_serializer = PillarProgramDisbursementSerializer(disbursement)
        res = {"data": disbursement_serializer.data, "message": "Disbursement created"}
        return Response(res, status=status.HTTP_200_OK)

    def get(self, request):
        _id = self.request.GET.get("pillar_program")
        if _id:
            disbursements = PillarProgramDisbursement.objects.filter(pillar_program_id=_id)
            disbursements_serializer = PillarProgramDisbursementSerializer(disbursements, many=True)
            res = {"data": disbursements_serializer.data}
            return Response(res)
        else:
            res = {"data": None, "message": "provide pillar program"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class PublicSectorDisbursementAPIView(APIView):
    def post(self, request):
        request_data = request.data
        amount = request_data["amount"]
        pillar_program_id = request_data["pillar_program"]
        public_sector_id = request_data["public_sector"]
        description = request_data["description"]
        pillar_program = None
        try:
            pillar_program = PillarProgram.objects.get(id=pillar_program_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid pillar_program id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        public_sector = None
        try:
            public_sector = PublicSector.objects.get(id=public_sector_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid public_sector id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        # check if pillar program has enough available funds for the disbursement
        if amount <= pillar_program.available_funds:
            disbursement = PublicSectorDisbursement.objects.create(amount=amount, pillar_program=pillar_program,
                                                                   public_sector=public_sector,
                                                                   description=description)
            # Decrement disbursed funds
            pillar_program.available_funds -= amount
            pillar_program.save()
            disbursement_serializer = SectorDisbursementSerializer(disbursement)
            res = {"data": disbursement_serializer.data, "message": "Disbursement created"}
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {"data": None, "message": "Insufficient Funds"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        _id = self.request.GET.get("public_sector")
        if _id:
            disbursements = PublicSectorDisbursement.objects.filter(public_sector_id=_id)
            disbursements_serializer = SectorDisbursementSerializer(disbursements, many=True)
            res = {"data": disbursements_serializer.data}
            return Response(res)
        else:
            res = {"data": None, "message": "provide public_sector"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class DistrictDisbursementAPIView(APIView):
    def post(self, request):
        request_data = request.data
        amount = request_data["amount"]
        district_id = request_data["district"]
        pillar_program_id = request_data["pillar_program"]
        public_sector_id = request_data["public_sector"]
        description = request_data["description"]

        district = None
        try:
            district = District.objects.get(id=district_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid district id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        pillar_program = None
        try:
            pillar_program = PillarProgram.objects.get(id=pillar_program_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid pillar_program id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        public_sector = None
        try:
            public_sector = PublicSector.objects.get(id=public_sector_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid public_sector id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        # check if public_sector has enough available funds for the disbursement
        if amount <= public_sector.available_funds:
            disbursement = DistrictDisbursement.objects.create(amount=amount, pillar_program=pillar_program,
                                                               public_sector=public_sector, description=description,
                                                               district=district)
            # Decrement disbursed funds
            public_sector.available_funds -= amount
            public_sector.save()
            disbursement_serializer = DistrictDisbursementSerializer(disbursement)
            res = {"data": disbursement_serializer.data, "message": "Disbursement created"}
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {"data": None, "message": "Insufficient Funds"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        _id = self.request.GET.get("district")
        if _id:
            disbursements = DistrictDisbursement.objects.filter(district_id=_id)
            disbursements_serializer = DistrictDisbursementSerializer(disbursements, many=True)
            res = {"data": disbursements_serializer.data}
            return Response(res)
        else:
            res = {"data": None, "message": "provide district"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class CountyDisbursementAPIView(APIView):
    def post(self, request):
        request_data = request.data
        amount = request_data["amount"]
        county_id = request_data["county"]
        pillar_program_id = request_data["pillar_program"]
        public_sector_id = request_data["public_sector"]
        description = request_data["description"]

        county = None
        try:
            county = County.objects.get(id=county_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid county"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        pillar_program = None
        try:
            pillar_program = PillarProgram.objects.get(id=pillar_program_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid pillar_program id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        public_sector = None
        try:
            public_sector = PublicSector.objects.get(id=public_sector_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid public_sector id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        # check if district has enough available funds for the disbursement
        district = District.objects.get(id=county.district_id)
        #get funds for this public sector
        if (district.available_funds.get(f"public_sector_{public_sector.id}") and
            amount <= district.available_funds.get(f"public_sector_{public_sector.id}")):
            disbursement = CountyDisbursement.objects.create(amount=amount, pillar_program=pillar_program,
                                                             public_sector=public_sector, description=description,
                                                             county=county)
            # Decrement disbursed funds
            district.available_funds["total_funds_available"] -= amount
            district.available_funds[f"public_sector_{public_sector.id}"] -= amount
            district.save()
            disbursement_serializer = CountyDisbursementSerializer(disbursement)
            res = {"data": disbursement_serializer.data, "message": "Disbursement created"}
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {"data": None, "message": "Insufficient Funds"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        _id = self.request.GET.get("county")
        if _id:
            disbursements = CountyDisbursement.objects.filter(county_id=_id)
            disbursements_serializer = CountyDisbursementSerializer(disbursements, many=True)
            res = {"data": disbursements_serializer.data}
            return Response(res)
        else:
            res = {"data": None, "message": "provide county"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class SubCountyDisbursementAPIView(APIView):
    def post(self, request):
        request_data = request.data
        amount = request_data["amount"]
        subcounty_id = request_data["subcounty"]
        pillar_program_id = request_data["pillar_program"]
        public_sector_id = request_data["public_sector"]
        description = request_data["description"]

        subcounty = None
        try:
            subcounty = SubCounty.objects.get(id=subcounty_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid subcounty"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        pillar_program = None
        try:
            pillar_program = PillarProgram.objects.get(id=pillar_program_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid pillar_program id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        public_sector = None
        try:
            public_sector = PublicSector.objects.get(id=public_sector_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid public_sector id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        # check if county has enough available funds for the disbursement in this sector
        county = County.objects.get(id=subcounty.county_id)
        if (county.available_funds.get(f"public_sector_{public_sector.id}") and
            amount <= county.available_funds.get(f"public_sector_{public_sector.id}")):
            disbursement = SubCountyDisbursement.objects.create(amount=amount, pillar_program=pillar_program,
                                                                public_sector=public_sector, description=description,
                                                                subcounty=subcounty)
            # Decrement disbursed funds
            county.available_funds["total_funds_available"] -= amount
            county.available_funds[f"public_sector_{public_sector.id}"] -= amount
            county.save()
            disbursement_serializer = SubCountyDisbursementSerializer(disbursement)
            res = {"data": disbursement_serializer.data, "message": "Disbursement created"}
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {"data": None, "message": "Insufficient Funds"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        _id = self.request.GET.get("subcounty")
        if _id:
            disbursements = SubCountyDisbursement.objects.filter(subcounty_id=_id)
            disbursements_serializer = SectorDisbursementSerializer(disbursements, many=True)
            res = {"data": disbursements_serializer.data}
            return Response(res)
        else:
            res = {"data": None, "message": "provide subcounty"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class ParishDisbursementAPIView(APIView):
    def post(self, request):
        request_data = request.data
        amount = request_data["amount"]
        parish_id = request_data["parish"]
        pillar_program_id = request_data["pillar_program"]
        public_sector_id = request_data["public_sector"]
        description = request_data["description"]

        parish = None
        try:
            parish = Parish.objects.get(id=parish_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid parish"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        pillar_program = None
        try:
            pillar_program = PillarProgram.objects.get(id=pillar_program_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid pillar_program id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        public_sector = None
        try:
            public_sector = PublicSector.objects.get(id=public_sector_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid public_sector id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        # check if subcounty has enough available funds for the disbursement
        subcounty = SubCounty.objects.get(id=parish.sub_county_id)
        if (subcounty.available_funds.get(f"public_sector_{public_sector.id}") and
            amount <= subcounty.available_funds.get(f"public_sector_{public_sector.id}")):
            disbursement = ParishDisbursement.objects.create(amount=amount, pillar_program=pillar_program,
                                                             public_sector=public_sector, description=description,
                                                             parish=parish)
            # Decrement disbursed funds
            subcounty.available_funds["total_funds_available"] -= amount
            subcounty.available_funds[f"public_sector_{public_sector.id}"] -= amount
            subcounty.save()
            disbursement_serializer = ParishDisbursementSerializer(disbursement)
            res = {"data": disbursement_serializer.data, "message": "Disbursement created"}
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {"data": None, "message": "Insufficient Funds"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        _id = self.request.GET.get("parish")
        if _id:
            disbursements = ParishDisbursement.objects.filter(parish_id=_id)
            disbursements_serializer = ParishDisbursementSerializer(disbursements, many=True)
            res = {"data": disbursements_serializer.data}
            return Response(res)
        else:
            res = {"data": None, "message": "provide parish"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class VillageDisbursementAPIView(APIView):
    def post(self, request):
        request_data = request.data
        amount = request_data["amount"]
        village_id = request_data["village"]
        pillar_program_id = request_data["pillar_program"]
        public_sector_id = request_data["public_sector"]
        description = request_data["description"]

        village = None
        try:
            village = Village.objects.get(id=village_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid village"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        pillar_program = None
        try:
            pillar_program = PillarProgram.objects.get(id=pillar_program_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid pillar_program id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        public_sector = None
        try:
            public_sector = PublicSector.objects.get(id=public_sector_id)
        except ObjectDoesNotExist:
            res = {"message": "Invalid public_sector id"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        # check if parish has enough available funds for the disbursement
        parish = Parish.objects.get(id=village.parish_id)
        if (parish.available_funds.get(f"public_sector_{public_sector.id}") and
            amount <= parish.available_funds.get(f"public_sector_{public_sector.id}")):
            disbursement = VillageDisbursement.objects.create(amount=amount, pillar_program=pillar_program,
                                                              public_sector=public_sector, description=description,
                                                              village=village)
            # Decrement disbursed funds
            parish.available_funds["total_funds_available"] -= amount
            parish.available_funds[f"public_sector_{public_sector.id}"] -= amount
            parish.save()
            disbursement_serializer = VillageDisbursementSerializer(disbursement)
            res = {"data": disbursement_serializer.data, "message": "Disbursement created"}
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {"data": None, "message": "Insufficient Funds"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        _id = self.request.GET.get("village")
        if _id:
            disbursements = VillageDisbursement.objects.filter(village_id=_id)
            disbursements_serializer = VillageDisbursementSerializer(disbursements, many=True)
            res = {"data": disbursements_serializer.data}
            return Response(res)
        else:
            res = {"data": None, "message": "provide village"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class UpdateDisbursementStatusAPIView(APIView):
    def post(self, request):
        request_data = request.data
        disbursement_id = request_data.get("disbursement")
        pillar_program_id = request_data.get("pillar_program")
        public_sector_id = request_data.get("public_sector")
        district_id = request_data.get("district")
        county_id = request_data.get("county")
        subcounty_id = request_data.get("subcounty")
        parish_id = request_data.get("parish")
        village_id = request_data.get("village")
        if pillar_program_id:
            pillar_program = None
            try:
                pillar_program = PillarProgram.objects.get(id=pillar_program_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid pillar program id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            disbursement = None
            try:
                disbursement = PillarProgramDisbursement.objects.get(id=disbursement_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid disbursement id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if disbursement.status == "DISBURSED":
                res = {"message": "Disbursement status already updated"}
                return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)

            disbursement.status = "DISBURSED"
            disbursement.save()
            # update totals
            pillar_program.available_funds += disbursement.amount
            pillar_program.save()
            res = {"message": "Disbursement Updated"}
            return Response(res, status=status.HTTP_200_OK)

        if public_sector_id:
            public_sector = None
            try:
                public_sector = PublicSector.objects.get(id=public_sector_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid public sector"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            disbursement = None
            try:
                disbursement = PublicSectorDisbursement.objects.get(id=disbursement_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid disbursement id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if disbursement.status == "DISBURSED":
                res = {"message": "Disbursement status already updated"}
                return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)

            disbursement.status = "DISBURSED"
            disbursement.save()
            # update totals
            public_sector.available_funds += disbursement.amount
            public_sector.save()
            res = {"message": "Disbursement Updated"}
            return Response(res, status=status.HTTP_200_OK)

        if district_id:
            district = None
            try:
                district = District.objects.get(id=district_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid district"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            public_sector = None
            disbursement = None
            try:
                disbursement = DistrictDisbursement.objects.get(id=disbursement_id)
                public_sector = disbursement.public_sector
            except ObjectDoesNotExist:
                res = {"message": "Invalid disbursement id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if disbursement.status == "DISBURSED":
                res = {"message": "Disbursement status had already been updated"}
                return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)

            # update totals
            # check if previous funds exist for the public_sector
            if district.available_funds.get(f"public_sector_{public_sector.id}"):
                district.available_funds[f"public_sector_{public_sector.id}"] += disbursement.amount
            else:
                district.available_funds[f"public_sector_{public_sector.id}"] = disbursement.amount
            district.available_funds[f"total_funds_available"] += disbursement.amount
            district.save()
            disbursement.status = "DISBURSED"
            disbursement.save()
            res = {"message": "Disbursement Updated"}
            return Response(res, status=status.HTTP_200_OK)

        if county_id:
            county = None
            try:
                county = County.objects.get(id=county_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid county"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            disbursement = None
            public_sector = None
            try:
                disbursement = CountyDisbursement.objects.get(id=disbursement_id)
                public_sector = disbursement.public_sector
            except ObjectDoesNotExist:
                res = {"message": "Invalid disbursement id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if disbursement.status == "DISBURSED":
                res = {"message": "Disbursement status already updated"}
                return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)

            # update totals
            # check if previous funds exist for the public_sector
            if county.available_funds.get(f"public_sector_{public_sector.id}"):
                county.available_funds[f"public_sector_{public_sector.id}"] += disbursement.amount
            else:
                county.available_funds[f"public_sector_{public_sector.id}"] = disbursement.amount
            county.available_funds[f"total_funds_available"] += disbursement.amount
            county.save()
            disbursement.status = "DISBURSED"
            disbursement.save()
            res = {"message": "Disbursement Updated"}
            return Response(res, status=status.HTTP_200_OK)

        if subcounty_id:
            subcounty = None
            try:
                subcounty = SubCounty.objects.get(id=subcounty_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid subcounty"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            disbursement = None
            public_sector = None
            try:
                disbursement = SubCountyDisbursement.objects.get(id=disbursement_id)
                public_sector = disbursement.public_sector
            except ObjectDoesNotExist:
                res = {"message": "Invalid disbursement id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if disbursement.status == "DISBURSED":
                res = {"message": "Disbursement status already updated"}
                return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)

            # update totals
            # check if previous funds exist for the public_sector
            if subcounty.available_funds.get(f"public_sector_{public_sector.id}"):
                subcounty.available_funds[f"public_sector_{public_sector.id}"] += disbursement.amount
            else:
                subcounty.available_funds[f"public_sector_{public_sector.id}"] = disbursement.amount
            subcounty.available_funds[f"total_funds_available"] += disbursement.amount
            subcounty.save()
            disbursement.status = "DISBURSED"
            disbursement.save()
            res = {"message": "Disbursement Updated"}
            return Response(res, status=status.HTTP_200_OK)

        if parish_id:
            parish = None
            try:
                parish = Parish.objects.get(id=parish_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid parish"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            disbursement = None
            public_sector = None
            try:
                disbursement = ParishDisbursement.objects.get(id=disbursement_id)
                public_sector = disbursement.public_sector
            except ObjectDoesNotExist:
                res = {"message": "Invalid disbursement id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if disbursement.status == "DISBURSED":
                res = {"message": "Disbursement status already updated"}
                return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)

            # update totals
            # check if previous funds exist for the public_sector
            if parish.available_funds.get(f"public_sector_{public_sector.id}"):
                parish.available_funds[f"public_sector_{public_sector.id}"] += disbursement.amount
            else:
                parish.available_funds[f"public_sector_{public_sector.id}"] = disbursement.amount
            parish.available_funds[f"total_funds_available"] += disbursement.amount
            parish.save()
            disbursement.status = "DISBURSED"
            disbursement.save()
            res = {"message": "Disbursement Updated"}
            return Response(res, status=status.HTTP_200_OK)

        if village_id:
            village = None
            try:
                village = Village.objects.get(id=village_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid village"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            disbursement = None
            public_sector = None
            try:
                disbursement = VillageDisbursement.objects.get(id=disbursement_id)
                public_sector = disbursement.public_sector
            except ObjectDoesNotExist:
                res = {"message": "Invalid disbursement id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if disbursement.status == "DISBURSED":
                res = {"message": "Disbursement status already updated"}
                return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)

            # update totals
            # check if previous funds exist for the public_sector
            if village.available_funds.get(f"public_sector_{public_sector.id}"):
                village.available_funds[f"public_sector_{public_sector.id}"] += disbursement.amount
            else:
                village.available_funds[f"public_sector_{public_sector.id}"] = disbursement.amount
            village.available_funds[f"total_funds_available"] += disbursement.amount
            village.save()
            disbursement.status = "DISBURSED"
            disbursement.save()
            res = {"message": "Disbursement Updated"}
            return Response(res, status=status.HTTP_200_OK)

        res = {"message": "Incomplete Request"}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        res = {"message": "OK"}
        return Response(res, status=status.HTTP_200_OK)

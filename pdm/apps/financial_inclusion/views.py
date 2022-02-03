from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from pdm.apps.demographics.serializers import *
from pdm.apps.financial_inclusion.models import *
from pdm.apps.financial_inclusion.serializers import *

from django.db.models import Sum


class OrganizationTypeAPIView(ListCreateAPIView):
    serializer_class = OrganizationTypeSerializer
    queryset = OrganizationType.objects.all()


class CommunityOrganizationAPIView(ListCreateAPIView):
    serializer_class = CommunityOrganizationSerializer
    queryset = CommunityOrganization.objects.all()


class InitiativeAPIView(ListCreateAPIView):
    serializer_class = InitiativeSerializer
    queryset = Initiative.objects.all()


class BusinessDevelopmentServiceAPIView(ListCreateAPIView):
    serializer_class = BusinessDevelopmentServiceSerializer
    queryset = BusinessDevelopmentService.objects.all()


class BeneficiariesSummariesView(APIView):
    def post(self, request):
        pass

    def get(self, request):
        district_id = request.GET.get("district")
        county_id = request.GET.get("county")
        subcounty_id = request.GET.get("subcounty")
        parish_id = request.GET.get("parish")

        if district_id:
            district = None
            try:
                district = District.objects.get(id=district_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid district id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            counties = County.objects.filter(district_id=district_id)
            sub_counties = SubCounty.objects.filter(county_id__in=counties)
            parishes = Parish.objects.filter(sub_county_id__in=sub_counties)
            villages = Village.objects.filter(parish_id__in=parishes)
            beneficiaries_count = CommunityOrganization.objects.filter(village_id__in=villages).count()
            district_serializer = DistrictSerializer(district)
            res = {"beneficiaries": beneficiaries_count, "county": district_serializer.data}
            return Response(res, status=status.HTTP_200_OK)
        if county_id:
            county = None
            try:
                county = County.objects.get(id=county_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid county id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            sub_counties = SubCounty.objects.filter(county_id=county_id)
            parishes = Parish.objects.filter(sub_county_id__in=sub_counties)
            villages = Village.objects.filter(parish_id__in=parishes)
            beneficiaries_count = CommunityOrganization.objects.filter(village_id__in=villages).count()
            county_serializer = CountySerializer(county)
            res = {"beneficiaries": beneficiaries_count, "county": county_serializer.data}
            return Response(res, status=status.HTTP_200_OK)
        if subcounty_id:
            subcounty = None
            try:
                subcounty = SubCounty.objects.get(id=subcounty_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid subcounty id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            parishes = Parish.objects.filter(sub_county_id=subcounty_id)
            villages = Village.objects.filter(parish_id__in=parishes)
            beneficiaries_count = CommunityOrganization.objects.filter(village_id__in=villages).count()
            subcounty_serializer = SubCountySerializer(subcounty)
            res = {"beneficiaries": beneficiaries_count, "subcounty": subcounty_serializer.data}
            return Response(res, status=status.HTTP_200_OK)
        if parish_id:
            parish = None
            try:
                parish = Parish.objects.get(id=parish_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid parish id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            beneficiaries_count = CommunityOrganization.objects.filter(village__parish_id=parish_id).count()
            parish_serializer = ParishSerializer(parish)
            res = {"beneficiaries": beneficiaries_count, "parish": parish_serializer.data}
            return Response(res, status=status.HTTP_200_OK)
        else:
            beneficiaries_count = CommunityOrganization.objects.all().count()
            res = {"total_beneficiaries": beneficiaries_count}
            return Response(res, status=status.HTTP_200_OK)


class SavingsAPIView(APIView):
    def get(self, request):
        savings = Saving.objects.all()
        serializer_class = SavingsSerializer(savings, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        request_data = request.data
        serializer = SavingsCreateSerializer(data=request_data)
        res = {}
        if serializer.is_valid():
            try:
                national_id = request_data.get("identification_no")
                farmer = Farmer.objects.get(user__identification_no=national_id)
                amount = request_data.get("amount")

                saving = Saving.objects.create(farmer=farmer, amount=amount)
                saving_serializer = SavingsSerializer(saving)
                res["msg"] = "Savings successfully recorded"
                res["success"] = True
                res["data"] = saving_serializer.data
                return Response(res, status=status.HTTP_201_CREATED)
            except Exception as e:
                res = {"success": False, "msg": str(e), "data": None}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        else:
            res = {"success": False, "msg": serializer.errors, "data": None}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class SavingsTotalAPIView(APIView):
    def get(self, request):
        district_id = request.GET.get("district")
        county_id = request.GET.get("county")
        subcounty_id = request.GET.get("subcounty")
        parish_id = request.GET.get("parish")

        if district_id:
            district = None
            try:
                district = District.objects.get(id=district_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid district id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            counties = County.objects.filter(district_id=district_id)

            total_district_savings = 0
            county_totals = []
            for county in counties:
                county_serializer = CountySerializer(county)
                subcounties = SubCounty.objects.filter(county_id=county.id)
                parishes = Parish.objects.filter(sub_county_id__in=subcounties)
                villages = Village.objects.filter(parish_id__in=parishes)
                farmers = Farmer.objects.filter(village_id__in=villages)
                savings = Saving.objects.filter(farmer_id__in=farmers)

                county_savings_total = savings.aggregate(Sum('amount')).get("amount__sum") if savings else 0
                county_totals.append({
                    "county": county_serializer.data,
                    "county_total": county_savings_total
                })
                total_district_savings += county_savings_total

            district_serializer = DistrictSerializer(district)
            res = {"district": district_serializer.data, "county_total": total_district_savings,
                   "counties": county_totals}
            return Response(res, status=status.HTTP_200_OK)

        if county_id:
            county = None
            try:
                county = County.objects.get(id=county_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid county id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            subcounties = SubCounty.objects.filter(county_id=county_id)

            total_county_savings = 0
            subcounty_totals = []
            for subcounty in subcounties:
                sub_county_serializer = SubCountySerializer(subcounty)
                parishes = Parish.objects.filter(sub_county_id=subcounty.id)
                villages = Village.objects.filter(parish_id__in=parishes)
                farmers = Farmer.objects.filter(village_id__in=villages)
                savings = Saving.objects.filter(farmer_id__in=farmers)

                subcounty_savings_total = savings.aggregate(Sum('amount')).get("amount__sum") if savings else 0
                subcounty_totals.append({
                    "subcounty": sub_county_serializer.data,
                    "sub_county_total": subcounty_savings_total
                })
                total_county_savings += subcounty_savings_total

            county_serializer = CountySerializer(county)
            res = {"county": county_serializer.data, "county_total": total_county_savings,
                   "subcounties": subcounty_totals}
            return Response(res, status=status.HTTP_200_OK)

        if subcounty_id:
            subcounty = None
            try:
                subcounty = SubCounty.objects.get(id=subcounty_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid subcounty id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            parishes = Parish.objects.filter(sub_county_id=subcounty_id)
            subcounty_total = 0
            parish_totals = []
            for parish in parishes:
                parish_serializer = ParishSerializer(parish)
                villages = Village.objects.filter(parish_id=parish.id)
                farmers = Farmer.objects.filter(village_id__in=villages)
                savings = Saving.objects.filter(farmer_id__in=farmers)

                parish_savings_total = savings.aggregate(Sum('amount')).get("amount__sum") if savings else 0
                parish_totals.append({
                    "parish": parish_serializer.data,
                    "parish_total": parish_savings_total
                })
                subcounty_total += parish_savings_total

            sub_county_serializer = SubCountySerializer(subcounty)
            res = {"subcounty": sub_county_serializer.data, "subcounty_total": subcounty_total,
                   "parishes": parish_totals}
            return Response(res, status=status.HTTP_200_OK)
        if parish_id:
            parish = None
            try:
                parish = Parish.objects.get(id=parish_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid parish id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            villages = Village.objects.filter(parish_id=parish_id)
            parish_total = 0
            village_totals = []
            for village in villages:
                village_serializer = VillageSerializer(village)
                farmers = Farmer.objects.filter(village_id=village.id)
                savings = Saving.objects.filter(farmer_id__in=farmers)
                parish_savings_total = savings.aggregate(Sum('amount')).get("amount__sum") if savings else 0
                village_totals.append({
                    "village": village_serializer.data,
                    "village_total": parish_savings_total
                })
                parish_total += parish_savings_total

            parish_serializer = ParishSerializer(parish)
            res = {"parish": parish_serializer.data, "parish_total": parish_total,
                   "villages": village_totals}
            return Response(res, status=status.HTTP_200_OK)

        districts = District.objects.all()

        total_national_savings = 0
        district_totals = []
        for district in districts:
            district_serializer = DistrictSerializer(district)
            counties = County.objects.filter(district_id=district.id)
            subcounties = SubCounty.objects.filter(county_id__in=counties)
            parishes = Parish.objects.filter(sub_county_id__in=subcounties)
            villages = Village.objects.filter(parish_id__in=parishes)
            farmers = Farmer.objects.filter(village_id__in=villages)
            savings = Saving.objects.filter(farmer_id__in=farmers)

            district_savings_total = savings.aggregate(Sum('amount')).get("amount__sum") if savings else 0
            district_totals.append({
                "district": district_serializer.data,
                "district_total": district_savings_total
            })
            total_national_savings += district_savings_total

        res = {"national_total": total_national_savings,
               "districts": district_totals}
        return Response(res, status=status.HTTP_200_OK)

    def post(self, request):
        pass


class BusinessDevelopmentServiceSummaryAPIView(APIView):
    def get(self, request):
        district_id = request.GET.get("district")
        county_id = request.GET.get("county")
        subcounty_id = request.GET.get("subcounty")
        parish_id = request.GET.get("parish")

        if district_id:
            district = None
            try:
                district = District.objects.get(id=district_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid district id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            counties = County.objects.filter(district_id=district_id)

            total_district_training = 0
            county_totals = []
            for county in counties:
                county_serializer = CountySerializer(county)
                subcounties = SubCounty.objects.filter(county_id=county.id)
                parishes = Parish.objects.filter(sub_county_id__in=subcounties)
                villages = Village.objects.filter(parish_id__in=parishes)
                trainings = BusinessDevelopmentService.objects.filter(village_id__in=villages)

                county_training_total = trainings.count()
                county_totals.append({
                    "county": county_serializer.data,
                    "county_total": county_training_total
                })
                total_district_training += county_training_total

            district_serializer = DistrictSerializer(district)
            res = {"district": district_serializer.data, "county_total": total_district_training,
                   "counties": county_totals}
            return Response(res, status=status.HTTP_200_OK)

        if county_id:
            county = None
            try:
                county = County.objects.get(id=county_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid county id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            subcounties = SubCounty.objects.filter(county_id=county_id)

            total_county_savings = 0
            subcounty_totals = []
            for subcounty in subcounties:
                sub_county_serializer = SubCountySerializer(subcounty)
                parishes = Parish.objects.filter(sub_county_id=subcounty.id)
                villages = Village.objects.filter(parish_id__in=parishes)
                trainings = BusinessDevelopmentService.objects.filter(village_id__in=villages)

                subcounty_trainings_total = trainings.count()
                subcounty_totals.append({
                    "subcounty": sub_county_serializer.data,
                    "sub_county_total": subcounty_trainings_total
                })
                total_county_savings += subcounty_trainings_total

            percentage_totals = [
                dict(item, percentage=round(item["sub_county_total"] / total_county_savings * 100, ndigits=2))
                for item in subcounty_totals]
            county_serializer = CountySerializer(subcounty)
            res = {"county": county_serializer.data, "county_total": total_county_savings,
                   "parishes": percentage_totals}
        if subcounty_id:
            subcounty = None
            try:
                subcounty = SubCounty.objects.get(id=subcounty_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid subcounty id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            parishes = Parish.objects.filter(sub_county_id=subcounty_id)
            subcounty_total = 0
            parish_totals = []
            for parish in parishes:
                parish_serializer = ParishSerializer(parish)
                villages = Village.objects.filter(parish_id=parish.id)
                trainings = BusinessDevelopmentService.objects.filter(village_id__in=villages)

                parish_trainings_total = trainings.count()
                parish_totals.append({
                    "parish": parish_serializer.data,
                    "parish_total": parish_trainings_total
                })
                subcounty_total += parish_trainings_total

            percentage_totals = [
                dict(item, percentage=round(item["parish_total"] / subcounty_total * 100, ndigits=2))
                for item in parish_totals]

            sub_county_serializer = SubCountySerializer(subcounty)
            res = {"subcounty": sub_county_serializer.data, "subcounty_total": subcounty_total,
                   "parishes": percentage_totals}
            return Response(res, status=status.HTTP_200_OK)
        if parish_id:
            parish = None
            try:
                parish = Parish.objects.get(id=parish_id)
            except ObjectDoesNotExist:
                res = {"message": "Invalid parish id"}
                return Response(res, status=status.HTTP_404_NOT_FOUND)
            villages = Village.objects.filter(parish_id=parish_id)
            parish_total = 0
            village_totals = []
            for village in villages:
                village_serializer = VillageSerializer(village)
                trainings = BusinessDevelopmentService.objects.filter(village_id__in=villages)
                village_training_total = trainings.count()
                village_totals.append({
                    "village": village_serializer.data,
                    "village_total": village_training_total
                })
                parish_total += village_training_total
            percentage_totals = [
                dict(item, percentage=round(item["village_total"] / parish_total * 100, ndigits=2))
                for item in village_totals]

            parish_serializer = ParishSerializer(parish)
            res = {"parish": parish_serializer.data, "parish_total": parish_total,
                   "villages": percentage_totals}
            return Response(res, status=status.HTTP_200_OK)

        # get national summary if filter parameter is not provided
        districts = District.objects.all()
        total_national_trainings = 0
        district_trainings = []
        for district in districts:
            district_serializer = DistrictSerializer(district)
            counties = County.objects.filter(district_id=district.id)
            subcounties = SubCounty.objects.filter(county_id__in=counties)
            parishes = Parish.objects.filter(sub_county_id__in=subcounties)
            villages = Village.objects.filter(parish_id__in=parishes)
            trainings = BusinessDevelopmentService.objects.filter(village_id__in=villages)

            district_trainings_total = trainings.count()
            district_trainings.append({
                "district": district_serializer.data,
                "district_trainings": district_trainings_total
            })
            total_national_trainings += district_trainings_total

        percentage_totals = [dict(item, percentage=round(item["district_trainings"]/total_national_trainings*100, ndigits=2)) for item in district_trainings]
        res = {"national_trainings": total_national_trainings,
               "districts": percentage_totals}
        return Response(res, status=status.HTTP_200_OK)

    def post(self, request):
        pass


class NationalDashboardAPIView(APIView):
    def post(self, request):
        pass

    def get(self, request):
        beneficiaries = CommunityOrganization.objects.all().count()
        trainings = BusinessDevelopmentService.objects.all().count()
        res = {
            "trainings": trainings,
            "beneficiaries": beneficiaries}
        return Response(res, status=status.HTTP_200_OK)

from django.urls import path
from .views import *

urlpatterns = [
    path("public-sector/", PublicSectorAPIView.as_view(), name="public_sector"),
    path("pillar-program/", PillarProgramAPIView.as_view(), name="pillar_program"),
    path("update-disbursement-status/", UpdateDisbursementStatusAPIView.as_view(), name="update_disbursement_status"),
    path("pillar-program-disbursement/", PillarProgramDisbursementAPIView.as_view(), name="pillar_program_disbursement"),
    path("public-sector-disbursement/", PublicSectorDisbursementAPIView.as_view(), name="public_sector_disbursement"),
    path("district-disbursement/", DistrictDisbursementAPIView.as_view(), name="district_disbursement"),
    path("county-disbursement/", CountyDisbursementAPIView.as_view(), name="county_disbursement"),
    path("subcounty-disbursement/", SubCountyDisbursementAPIView.as_view(), name="subcounty_disbursement"),
    path("parish-disbursement/", ParishDisbursementAPIView.as_view(), name="parish_disbursement"),
    path("village-disbursement/", VillageDisbursementAPIView.as_view(), name="village_disbursement"),
]

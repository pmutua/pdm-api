from django.urls import path
from .views import *

urlpatterns = [
    path("districts/", DistrictAPIView.as_view(), name="districts"),
    path("district/<int:pk>", DistrictDetailAPIView.as_view(), name="district-detail"),
    path("counties/", CountyAPIView.as_view(), name="counties"),
    path("county/<int:pk>", CountyDetailAPIView.as_view(), name="county-detail"),
    path("subcounties/", SubCountyAPIView.as_view(), name="sub-counties"),
    path("subcounty/<int:pk>", SubCountyDetailAPIView.as_view(), name="sub-county-detail"),
    path("parishes/", ParishAPIView.as_view(), name="parishes"),
    path("parish/<int:pk>", ParishDetailAPIView.as_view(), name="parish-detail"),
    path("villages/", VillageAPIView.as_view(), name="villages"),
    path("village/", VillageDetailAPIView.as_view(), name="village-detail"),
    path("village/<int:pk>", VillageDetailAPIView.as_view(), name="village-detail"),
    path("district-spending", DistrictSpendingAPIView.as_view(), name="district_spending"),
    path("parish-dashboard", ParishDashboardAPIView.as_view(), name="parish_dashboards"),
]

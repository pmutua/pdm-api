from django.urls import path
from .views import *

urlpatterns = [
    path("organization-types/", OrganizationTypeAPIView.as_view(), name="organization_types"),
    path("community-organizations/", CommunityOrganizationAPIView.as_view(), name="community_organizations"),
    path("initiatives/", InitiativeAPIView.as_view(), name="initiatives"),
    path("beneficiaries-summary/", BeneficiariesSummariesView.as_view(), name="beneficiaries_summary"),
    path("business-development-services/", BusinessDevelopmentServiceAPIView.as_view(), name="business_development_services"),
    path("savings/", SavingsAPIView.as_view(), name="savings"),
    path("savings-total/", SavingsTotalAPIView.as_view(), name="savings_total"),
    path("national-dashboard/", NationalDashboardAPIView.as_view(), name="national_dashboard"),
    path("trainings-dashboard/national", BusinessDevelopmentSummaryNationalPieChartAPIView.as_view(), name="trainings_national_dashboard"),
]

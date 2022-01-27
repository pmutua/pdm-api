from django.urls import path
from .views import *

urlpatterns = [
    path("organization-types/", OrganizationTypeAPIView.as_view(), name="organization_types"),
    path("community-organizations/", CommunityOrganizationAPIView.as_view(), name="community_organizations"),
    path("initiatives/", InitiativeAPIView.as_view(), name="initiatives"),
    path("business-development-services/", BusinessDevelopmentServiceAPIView.as_view(), name="business_development_services"),
]

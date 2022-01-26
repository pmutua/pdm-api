from django.urls import path
from pdm.apps.farmers.views import (
    RegisterFarmerAPIView
)


urlpatterns = [
    path('register_farmer', RegisterFarmerAPIView.as_view(), name = "register-farmer")
]

from django.urls import path
from pdm.apps.farmers.views import *

urlpatterns = [
    path('', FarmersAPIView.as_view(), name="farmers"),
    path('register_farmer', RegisterFarmerAPIView.as_view(), name="register-farmer"),
]

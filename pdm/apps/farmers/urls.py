from django.urls import path
from pdm.apps.farmers.views import (
    FarmersAPIView,
    RegisterFarmerAPIView,
    CropAPIView,
    RecordProduceAPIview
)

urlpatterns = [
    path('', FarmersAPIView.as_view(), name="farmers"),
    path('register_farmer', RegisterFarmerAPIView.as_view(), name="register-farmer"),
    path('crops', CropAPIView.as_view(), name="crops"),
    path('produce/add', CropAPIView.as_view(), name="add-produce"),
]

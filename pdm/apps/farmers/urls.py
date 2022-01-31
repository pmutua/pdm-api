from django.urls import path
from pdm.apps.farmers.views import (
    FarmersAPIView,
    RegisterFarmerAPIView,
    CropAPIView,
    RecordProduceAPIview,
    ProduceDataAPIView,
    ProduceDataFilterByDistrictAPIView
)

urlpatterns = [
    path('', FarmersAPIView.as_view(), name="farmers"),
    path('register_farmer', RegisterFarmerAPIView.as_view(), name="register-farmer"),
    path('crops', CropAPIView.as_view(), name="crops"),
    path('produce/add', RecordProduceAPIview.as_view(), name="add-produce"),
    path('produce/data', ProduceDataAPIView.as_view(), name="produce-datas"),
    path('produce/district/data/', ProduceDataFilterByDistrictAPIView.as_view(), name="produce-district-data"),
]

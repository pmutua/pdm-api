from django.urls import path
from pdm.apps.farmers.views import *

urlpatterns = [
    path('', FarmersAPIView.as_view(), name="farmers"),
    path('register-farmer', RegisterFarmerView.as_view(), name="register_farmer"),
    path('crops', CropAPIView.as_view(), name="crops"),
    path('produce/add', RecordProduceAPIview.as_view(), name="add-produce"),
    path('produce/data', ProduceDataAPIView.as_view(), name="produce-datas"),
    path('produce/district/data/', ProduceDataFilterByDistrictAPIView.as_view(), name="produce-district-data"),
    path('produce/county/data/', ProduceDataFilterByCountyAPIView.as_view(), name="produce-county-data"),
    path('produce/sub-county/data/', ProduceDataFilterBySubCountyAPIView.as_view(), name="produce-sub-county-data"),
    path('produce/parish/data/', ProduceDataFilterByParishAPIView.as_view(), name="produce-parish-data"),
]

from django.urls import path
from .views import (
DistrictAPIView,
DistrictDetailAPIView
)

urlpatterns = [
    path('districts/', DistrictAPIView.as_view(), name='districts'),
    path('district/<int:pk>', DistrictDetailAPIView.as_view(), name = "district-detail")
]

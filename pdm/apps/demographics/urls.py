from django.urls import path
from .views import (
DistrictAPIView
)

urlpatterns = [
    path('districts/', DistrictAPIView.as_view(), name='districts')
]

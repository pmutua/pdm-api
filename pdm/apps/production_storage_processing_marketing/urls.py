from django.urls import path
from pdm.apps.production_storage_processing_marketing.views import *

urlpatterns = [
    path('evouchers', EvouchersAPIView.as_view(), name="evouchers"),
    path('dashboard', DashBoardApiView.as_view(), name="dashboard")
]

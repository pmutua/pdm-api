from django.urls import path
from django.views.decorators.cache import cache_page
from pdm.apps.production_storage_processing_marketing.views import *

urlpatterns = [
    path('evouchers', EvouchersAPIView.as_view(), name="evouchers"),
    path('dashboard', cache_page(60*5)(DashBoardApiView.as_view()), name="dashboard"),
]

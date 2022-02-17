from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('mindset-champions/', MindSetChampionView.as_view(), name="mindset_champions"),
]

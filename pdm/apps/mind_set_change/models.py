from django.db import models
from pdm.apps.pillar_management.models import PillarProgram
from pdm.apps.production_storage_processing_marketing.models import Evoucher
from pdm.apps.farmers.models import  Farmer
from pdm.apps.demographics.models import District
from model_utils.models import TimeStampedModel


class MindSetChampion(TimeStampedModel):
    """Represents mindset champion"""
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class CommunityMobilization(TimeStampedModel):
    """Represents community mobilization"""
    budget_spend = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    evouchers = models.ForeignKey(Evoucher, on_delete=models.CASCADE, null=True)


class EconomicEnhancementSupport(TimeStampedModel):
    """Represents economic enhancement support"""
    budget_spend = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    farmers = models.ForeignKey(Farmer, on_delete=models.CASCADE, blank=True)



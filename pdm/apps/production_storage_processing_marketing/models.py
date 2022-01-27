from django.db import models
from pdm.apps.pillar_management.models import PillarProgram
from pdm.apps.farmers.models import Farmer
from model_utils.models import TimeStampedModel


class Evoucher(TimeStampedModel):
    """
    Represents an e-Voucher for farm inputs
    """

    beneficiary = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True)
    voucher_no = models.CharField(max_length=200, null=True)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    farm_input = models.TextField(null=True)

    def __str__(self):
        return self.beneficiary.user.first_name + " " + self.beneficiary.user.last_name


class PSPMPillarProgram(PillarProgram):
    """Represents Pillar Program"""
    evouchers = models.ManyToManyField(Evoucher, blank=True)
    farmers = models.ManyToManyField(Farmer, blank=True)

    def __str__(self):
        return self.name

from django.db import models
from model_utils.models import TimeStampedModel
from pdm.apps.demographics.models import Village
from pdm.apps.pillar_management.models import PillarProgram


class OrganizationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CommunityOrganization(TimeStampedModel):
    """Represents communities e.g Youth Groups, SACCOs e.t.c"""
    name = models.CharField(max_length=100)
    organization_type = models.ForeignKey(OrganizationType,on_delete=models.CASCADE)
    village = models.ForeignKey(Village,on_delete=models.CASCADE,null=True)
    key_personel = models.CharField(max_length=250)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Initiative(models.Model):
    """represents government initiative e.g. Capacity Building"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BusinessDevelopmentService(TimeStampedModel):
    """Represents training sessions held."""
    initiative = models.ForeignKey(Initiative,on_delete=models.CASCADE,null=True)
    village = models.ForeignKey(Village,on_delete=models.CASCADE,null=True)
    budget_spend = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    attendance = models.IntegerField(null=True)
    date = models.DateField(blank=True,null=True)
    topic = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.initiative.name


class FinancialInclusionPillar(PillarProgram):
    """
    TODO: Add managers for getting:
     - No. of beneficiaries
     - Income value from processing
     - training sessions held
    """
    pass




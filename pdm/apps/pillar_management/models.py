from django.db import models
from model_utils.models import TimeStampedModel


class PublicSector(TimeStampedModel):
    """Represents a Public Sector. Ministry of Water etc"""

    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name + "" + self.code


class PillarProgramStatus(models.Model):
    """Represents pillar program status"""

    name = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name

class PillarProgram(TimeStampedModel):
    """Represents Pillar Program"""

    name = models.CharField(max_length=250, null=True)
    sector = models.ForeignKey(PublicSector, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True)
    commencement_date = models.DateField(null=True)
    status = models.ForeignKey(PublicSector, on_delete=models.CASCADE, null=True, blank=True)
    start_year = models.IntegerField(null=True)
    funds_disbursed = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    def __str__(self):
        return self.name

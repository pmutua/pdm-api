from django.db import models
from model_utils.models import TimeStampedModel

from pdm.apps.demographics.models import *


class PublicSector(TimeStampedModel):
    """Represents a Public Sector. Ministry of Water etc"""

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    available_funds = models.FloatField(default=0.00)

    def __str__(self):
        return f"{self.name} - {self.code}"


class PillarProgram(TimeStampedModel):
    """Represents Pillar Program"""
    # TODO: Track commencement date

    name = models.CharField(max_length=250)
    description = models.TextField(null=True)
    start_year = models.DateField(blank=True, null=True)
    available_funds = models.FloatField(default=0.00)

    def __str__(self):
        return self.name


class PillarProgramDisbursement(TimeStampedModel):
    pillar_program = models.ForeignKey(PillarProgram, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("DISBURSED", "Disbursed"),
    )
    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.pillar_program.name} - {self.amount}"


class PublicSectorDisbursement(TimeStampedModel):
    public_sector = models.ForeignKey(PublicSector, on_delete=models.DO_NOTHING)
    pillar_program = models.ForeignKey(PillarProgram, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    description = models.TextField()
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("DISBURSED", "Disbursed"),
    )
    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.public_sector.name} ({self.pillar_program.name}) - {self.amount}"


class DistrictDisbursement(TimeStampedModel):
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING)
    public_sector = models.ForeignKey(PublicSector, on_delete=models.DO_NOTHING)
    pillar_program = models.ForeignKey(PillarProgram, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    description = models.TextField()
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("DISBURSED", "Disbursed"),
    )
    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.district.name} ({self.public_sector.name}) - {self.amount}"


class CountyDisbursement(TimeStampedModel):
    county = models.ForeignKey(County, on_delete=models.DO_NOTHING)
    public_sector = models.ForeignKey(PublicSector, on_delete=models.DO_NOTHING)
    pillar_program = models.ForeignKey(PillarProgram, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    description = models.TextField()
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("DISBURSED", "Disbursed"),
    )
    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.county.name} ({self.public_sector.name}) - {self.amount}"


class SubCountyDisbursement(TimeStampedModel):
    subcounty = models.ForeignKey(SubCounty, on_delete=models.DO_NOTHING)
    public_sector = models.ForeignKey(PublicSector, on_delete=models.DO_NOTHING)
    pillar_program = models.ForeignKey(PillarProgram, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    description = models.TextField()
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("DISBURSED", "Disbursed"),
    )
    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.subcounty.name} ({self.public_sector.name}) - {self.amount}"


class ParishDisbursement(TimeStampedModel):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    public_sector = models.ForeignKey(PublicSector, on_delete=models.DO_NOTHING)
    pillar_program = models.ForeignKey(PillarProgram, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    description = models.TextField()
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("DISBURSED", "Disbursed"),
    )
    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.parish.name} ({self.public_sector.name}) - {self.amount}"


class VillageDisbursement(TimeStampedModel):
    village = models.ForeignKey(Village, on_delete=models.DO_NOTHING)
    public_sector = models.ForeignKey(PublicSector, on_delete=models.DO_NOTHING)
    pillar_program = models.ForeignKey(PillarProgram, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    description = models.TextField()
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("DISBURSED", "Disbursed"),
    )
    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.village.name} ({self.public_sector.name}) - {self.amount}"

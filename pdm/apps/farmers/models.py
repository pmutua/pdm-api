from django.db import models
from model_utils.models import TimeStampedModel
from pdm.apps.authentication.models import User
from pdm.apps.demographics.models import Village



class Crop(models.Model):
    """Represents the crops the farmer produces"""

    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Farmer(TimeStampedModel):
    """Represents a Farmer
     A farmer register will be developed and rolled-out in all parishes
    across the country to be managed by the parish chiefs, which will aid in building a
    national database of all farming households and regularly monitor their progress.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
    crops = models.ManyToManyField(Crop, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name



class Produce(TimeStampedModel):
    """Represents farmer's produce"""

    PRODUCE_STATE = (
        ('sold','sold'),
        ('market','market'),
        ('storage','storage'),
    )
    owner = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True)
    produce_in =models.CharField(max_length=10, choices=PRODUCE_STATE)
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.crop.name

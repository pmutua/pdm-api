# Python core imports
import uuid

# Django imports
from django.contrib.auth.models import (
    Group,
    AbstractUser,
)
from django.conf import settings
from django.db import models

# Phone validator
from django.core.validators import RegexValidator

# Third Party Imports
import pytz

utc = pytz.UTC


class Department(Group):
    """Represents department or ministry"""

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="department_users", blank=True)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name + "ID-" + str(self.id)


class User(AbstractUser):
    """Represents User class model"""

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,14}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.",
    )
    id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True)
    org_id = models.IntegerField(null=True, blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    identification_no = models.CharField(max_length=100, blank=True, null=True)
    first_login = models.BooleanField(default=False)

    def __str__(self):

        if self.id is None:
            return "N/A"
        return f"{self.first_name} {self.last_name}"

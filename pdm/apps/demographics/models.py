from django.db import models


class District(models.Model):
    """Represents a district"""

    name = models.CharField(max_length=50)
    available_funds = models.JSONField(default=dict({"total_funds_available": 0}))

    class Meta:
        app_label = "demographics"

    def __str__(self):
        return self.name


class County(models.Model):
    """Represents a County Model"""

    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, related_name="counties", on_delete=models.CASCADE, null=True)
    available_funds = models.JSONField(default=dict({"total_funds_available": 0}))

    class Meta:
        app_label = "demographics"

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    """Represents a SubCounty"""

    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, related_name="sub_counties", on_delete=models.CASCADE, null=True)
    available_funds = models.JSONField(default=dict({"total_funds_available": 0}))

    class Meta:
        app_label = "demographics"

    def     __str__(self):
        return self.name


class Parish(models.Model):
    """Represents a Parish"""

    name = models.CharField(max_length=50)
    sub_county = models.ForeignKey(SubCounty, related_name="parishes", on_delete=models.CASCADE, null=True)
    available_funds = models.JSONField(default=dict({"total_funds_available": 0}))

    class Meta:
        app_label = "demographics"

    def __str__(self):
        return self.name


class Village(models.Model):
    """Represents a village"""

    name = models.CharField(max_length=50)
    parish = models.ForeignKey(Parish, related_name="villages", on_delete=models.CASCADE, null=True)
    available_funds = models.JSONField(default=dict({"total_funds_available": 0}))

    class Meta:
        app_label = "demographics"

    def __str__(self):
        return self.name

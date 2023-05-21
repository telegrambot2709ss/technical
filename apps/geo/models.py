from django.db import models

from apps.geo import default_name


# For Task 8
class Region(models.Model):
    name = models.JSONField(default=default_name)
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name.get('name_uz')}"

    class Meta:
        verbose_name_plural = "Regions"
        ordering = ["ordering"]


class District(models.Model):
    name = models.JSONField(default=default_name)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="district_region"
    )
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name.get('name_uz')}"

    class Meta:
        verbose_name_plural = "Districts"
        ordering = ["ordering"]


class Village(models.Model):
    name = models.JSONField(default=default_name)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="village_district"
    )
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name.get('name_uz')}"

    class Meta:
        verbose_name_plural = "Villages"
        ordering = ["ordering"]

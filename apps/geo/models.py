from django.db import models

from apps.geo.utils import create_name_slug
from apps.geo import default_name


# For Task 8
class Region(models.Model):
    name = models.JSONField(default=default_name)
    slug = models.SlugField(
        unique=True, max_length=255, allow_unicode=True, null=True
    )
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name.get('name_uz')}"

    class Meta:
        verbose_name_plural = "Regions"
        ordering = ["ordering"]

    def save(self, *args, **kwargs):
        self.slug = create_name_slug(self)
        return super().save(*args, **kwargs)


class District(models.Model):
    name = models.JSONField(default=default_name)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="district_region"
    )
    slug = models.SlugField(
        unique=True, max_length=255, allow_unicode=True, null=True, blank=True
    )
    ordering = models.IntegerField(default=1)

    @property
    def parent(self):
        return self.region

    def __str__(self):
        return f"{self.name.get('name_uz')}"

    class Meta:
        verbose_name_plural = "Districts"
        ordering = ["ordering"]

    def save(self, *args, **kwargs):
        self.slug = create_name_slug(self)
        return super().save(*args, **kwargs)


class Village(models.Model):
    name = models.JSONField(default=default_name)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="village_district"
    )
    slug = models.SlugField(
        unique=True, max_length=255, allow_unicode=True, null=True, blank=True
    )
    ordering = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name.get('name_uz')}"

    class Meta:
        verbose_name_plural = "Villages"
        ordering = ["ordering"]

    def save(self, *args, **kwargs):
        self.slug = create_name_slug(self)
        return super().save(*args, **kwargs)

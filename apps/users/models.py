from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _


# User model For Task 1
class User(AbstractBaseUser, PermissionsMixin):
    """ Project User model"""

    username = models.CharField(
        max_length=255, unique=True, help_text=_("Username")
    )
    email = models.EmailField(
        max_length=255, unique=True, null=True, blank=True, help_text=_("User email")
    )
    fullname = models.CharField(
        max_length=100, null=True, blank=True, help_text=_("User Full name")
    )
    user_photo = models.ImageField(upload_to="users_photos/", null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, help_text=_("Date of registration"))
    is_active = models.BooleanField("is_active", default=True)
    is_staff = models.BooleanField("is_staff", default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.fullname}"

    def get_full_name(self):
        return f"{self.username}"

    def get_short_name(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']


# Sponsor model for Task 2
class Sponsor(models.Model):
    """ Project Sponsors """

    class SponsorType(models.TextChoices):
        PHYSICAL = "PHYSICAL", _("Physical person")
        LEGAL = "LEGAL", _("Legal entity")

    class Status(models.TextChoices):
        NEW = "NEW", _("New")
        MODERATION = "MODERATION", _("In moderation")
        CANCELED = "CANCELED", _("Canceled")
        CONFIRMED = "CONFIRMED", _("Confirmed")

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="sponsor"
    )
    sponsor_type = models.CharField(
        max_length=15, choices=SponsorType.choices, default=SponsorType.LEGAL
    )
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.MODERATION
    )
    summa = models.BigIntegerField(
        help_text=_("Sponsorship amount"), null=False, blank=False
    )
    organization = models.CharField(
        help_text=_("Organization name"), max_length=200, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = "Sponsors"
        ordering = ['-user__date_joined']


# Student model for Task 3
class Student(models.Model):
    class Status(models.TextChoices):
        BACHELOR = "BACHELOR", _("Bachelor")
        MAGISTER = "MAGISTER", _("Magister")

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student"
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.BACHELOR
    )
    university = models.CharField(max_length=255, help_text=_("Student University name"))
    contract = models.BigIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = "Students"
        ordering = ['-user__date_joined']

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user template extending the AbstractUser template.

    Additional attributes:
        birth_date (DateField): The user’s birth date.
        can_be_contacted (BooleanField): Indicates whether the user agrees to
        e contacted.
        can_data_be_shared (BooleanField): Indicates whether the user allows
        their data to be shared.
    """
    birth_date = models.DateField()
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

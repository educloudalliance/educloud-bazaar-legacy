from django.db import models
from django.utils import timezone

from oscar.core import compat
from oscar.apps.customer.abstract_models import AbstractUser

class User(AbstractUser):
    oid = models.CharField(max_length=255)
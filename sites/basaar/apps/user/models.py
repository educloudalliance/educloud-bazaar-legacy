from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oscar.core import compat
from oscar.apps.customer.abstract_models import AbstractUser

class User(AbstractUser):
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ])
    oid = models.CharField(max_length=255, blank=True)
    mepinId = models.CharField(max_length=255, blank=True)
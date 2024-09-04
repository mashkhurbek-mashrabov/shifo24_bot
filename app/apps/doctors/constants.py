from django.db import models
from django.utils.translation import gettext_lazy as _


class DayChoices(models.TextChoices):
    MON = 'mon', _('Monday')
    TUE = 'tue', _('Tuesday')
    WED = 'wed', _('Wednesday')
    THU = 'thu', _('Thursday')
    FRI = 'fri', _('Friday')
    SAT = 'sat', _('Saturday')
    SUN = 'sun', _('Sunday')


class DoctorStatusChoices(models.TextChoices):
    PENDING = 'pending', _('Pending')
    ACTIVE = 'active', _('Active')
    INACTIVE = 'inactive', _('Inactive')
    REJECTED = 'rejected', _('Rejected')

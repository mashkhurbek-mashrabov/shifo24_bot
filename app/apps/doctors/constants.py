from django.db import models
from django.utils.translation import gettext_lazy as _


class DayChoices(models.TextChoices):
    MON = 'Mon', _('Monday')
    TUE = 'Tue', _('Tuesday')
    WED = 'Wed', _('Wednesday')
    THU = 'Thu', _('Thursday')
    FRI = 'Fri', _('Friday')
    SAT = 'Sat', _('Saturday')
    SUN = 'Sun', _('Sunday')


class DoctorStatusChoices(models.TextChoices):
    PENDING = 'Pending', _('Pending')
    ACTIVE = 'Active', _('Active')
    INACTIVE = 'Inactive', _('Inactive')
    REJECTED = 'Rejected', _('Rejected')

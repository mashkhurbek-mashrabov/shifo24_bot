from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatusChoices(models.TextChoices):
    PENDING = 'pending', _('Pending')
    ACCEPTED = 'accepted', _('Accepted')
    COMPLETED = 'completed', _('Completed')
    CANCELLED = 'cancelled', _('Cancelled')
    REJECTED = 'rejected', _('Rejected')

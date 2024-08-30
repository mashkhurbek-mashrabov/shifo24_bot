from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from common.models.base import BaseModelV2
from .constants import OrderStatusChoices
from doctors.constants import DoctorStatusChoices


class Order(BaseModelV2):
    user = models.ForeignKey(
        'bot.TelegramUser',
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='orders'
    )
    doctor = models.ForeignKey(
        'doctors.Doctor',
        verbose_name=_('Doctor'),
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        limit_choices_to={'status': DoctorStatusChoices.ACTIVE}
    )
    specialization = models.ForeignKey(
        'common.Specialization',
        verbose_name=_('Specialization'),
        on_delete=models.SET_NULL,
        related_name='orders',
        limit_choices_to={'is_active': True, 'children__isnull': True},
        null=True
    )
    scheduled_date = models.DateTimeField(_('Scheduled date'))
    status = models.CharField(
        _('Status'),
        max_length=10,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING
    )
    note = models.TextField(_('Note'), null=True, blank=True, validators=[MaxLengthValidator(1000)])

    class Meta:
        verbose_name = _('Queue')
        verbose_name_plural = _('Queues')
        ordering = ['scheduled_date']

    def __str__(self):
        return f'{self.user} - {self.doctor} - {self.scheduled_date}'

    def save(self, *args, **kwargs):
        # Scheduled date validation, it should be only future date
        if not self.scheduled_date and self.scheduled_date and self.scheduled_date <= timezone.now():
            raise ValidationError({'scheduled_date': _('The scheduled date must be in the future.')})
        super().save(*args, **kwargs)


    @property
    def formatted_date(self):
        if self.scheduled_date:
            return self.scheduled_date.strftime('%H:%M %d.%m.%Y')
        return '-'
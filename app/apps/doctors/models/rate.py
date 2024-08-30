from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from common.models.base import BaseModelV2
from order.constants import OrderStatusChoices
from doctors.constants import DoctorStatusChoices


class Rate(BaseModelV2):
    doctor = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.CASCADE,
        related_name='rates',
        verbose_name=_('Doctor'),
        limit_choices_to={'status': DoctorStatusChoices.ACTIVE}
    )
    user = models.ForeignKey(
        'bot.TelegramUser',
        on_delete=models.SET_NULL,
        related_name='rates',
        verbose_name=_('User'),
        null=True
    )
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.SET_NULL,
        related_name='rates',
        verbose_name=_('Queue'),
        limit_choices_to={'status': OrderStatusChoices.COMPLETED},
        null=True
    )
    rate = models.PositiveSmallIntegerField(
        _('Rate'),
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rates')
        unique_together = ('doctor', 'user', "order")

    def __str__(self):
        return f'{self.doctor} - {self.user}'

    # user and user of the order should be the same
    def clean(self):
        super().clean()
        if self.user != self.order.user:
            raise ValidationError(_('User and user of the order should be the same'), code='invalid')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

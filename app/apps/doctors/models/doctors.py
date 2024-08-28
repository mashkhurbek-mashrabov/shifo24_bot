from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, MaxLengthValidator

from common.models.base import BaseModelV2
from doctors.constants import DayChoices, DoctorStatusChoices


class Doctor(BaseModelV2):
    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=30)
    photo = models.ImageField(
        _('Photo'),
        upload_to='doctors/photo/',
        null=True, blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    photo_telegram_id = models.CharField(
        _('Photo telegram id'),
        max_length=60,
        null=True,
        blank=True, unique=True,
    )
    phone_number = models.CharField(_('Phone number'), max_length=13, null=True, blank=True)
    telegram_id = models.CharField(_('Telegram id'), max_length=20, null=True, blank=True, unique=True)
    address = models.CharField(_('Address'), max_length=200, null=True, blank=True)
    lat = models.FloatField(_('Latitude'), null=True, blank=True)
    lng = models.FloatField(_('Longitude'), null=True, blank=True)
    lunch_start_time = models.TimeField(_('Lunch start time'), null=True, blank=True)
    lunch_end_time = models.TimeField(_('Lunch end time'), null=True, blank=True)
    specialization = models.ManyToManyField('common.Specialization', verbose_name=_('Specializations'),
                                            related_name='doctors', blank=True,
                                            limit_choices_to={'is_active': True,
                                                              'children__isnull': True})
    status = models.CharField(
        _('Status'),
        max_length=10,
        choices=DoctorStatusChoices.choices,
        default=DoctorStatusChoices.PENDING
    )
    bio = models.TextField(
        _('Bio'),
        null=True, blank=True,
        validators=[MaxLengthValidator(1000)]
    )

    class Meta:
        verbose_name = _('Doctor')
        verbose_name_plural = _('Doctors')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class WorkSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='work_schedules', on_delete=models.CASCADE)
    day = models.CharField(_('Day'), max_length=3, choices=DayChoices.choices)
    start_time = models.TimeField(_('Start time'))
    end_time = models.TimeField(_('End time'))

    class Meta:
        verbose_name = _('Work schedule')
        verbose_name_plural = _('Work schedules')
        unique_together = ('doctor', 'day')

    def __str__(self):
        return f"{self.doctor} | {DayChoices(self.day).label}"

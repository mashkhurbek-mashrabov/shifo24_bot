from django.db import models
from django.utils.translation import gettext_lazy as _

from common.manager import SpecializationManager


class Specialization(models.Model):
    name_uz = models.CharField(_('Name (Uz)'), max_length=100, unique=True)
    name_en = models.CharField(_('Name (En)'), max_length=100, unique=True)
    name_ru = models.CharField(_('Name (Ru)'), max_length=100, unique=True)
    parent = models.ForeignKey(verbose_name=_('Parent'), to='self', related_name='children', on_delete=models.CASCADE,
                               null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = SpecializationManager()

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'
        ordering = ['order']

    def save(self, *args, **kwargs):
        # auto set order if it is not set
        if self.order is None:
            max_order = Specialization.objects.filter(parent=self.parent).aggregate(models.Max('order'))['order__max']
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

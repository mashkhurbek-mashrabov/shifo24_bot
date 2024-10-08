from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DoctorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctors'

    verbose_name = _('Doctors')
    verbose_name_plural = _('Doctors')

    def ready(self):
        from . import signals  # noqa

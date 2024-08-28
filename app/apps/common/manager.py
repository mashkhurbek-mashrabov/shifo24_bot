from django.db import models


class SpecializationManager(models.Manager):
    def get_active(self):
        return self.get_queryset().filter(is_active=True)

    def get_parents(self):
        return self.get_queryset().filter(parent__isnull=True)

import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .models.doctors import Doctor


@receiver(post_delete, sender=Doctor)
def delete_doctor_photo_on_delete(sender, instance, **kwargs):
    """
    Delete the doctor photo file from filesystem
     when the corresponding `Doctor` object is deleted
    """
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


@receiver(pre_save, sender=Doctor)
def delete_doctor_photo_on_update_photo(sender, instance, **kwargs):
    """
    Delete the doctor photo file from filesystem
     when the corresponding `Doctor` object's photo is updated
    """
    if not instance.pk:
        return False

    try:
        old_doctor = Doctor.objects.get(pk=instance.pk)
    except Doctor.DoesNotExist:
        return False

    if not old_doctor.photo == instance.photo:
        if os.path.isfile(old_doctor.photo.path):
            os.remove(old_doctor.photo.path)
        instance.photo_telegram_id = None

    return True

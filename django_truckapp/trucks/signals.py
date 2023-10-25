from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MaintenanceLog


@receiver(post_save, sender=MaintenanceLog)
def create_log_number_on_save(sender, instance, created, **kwargs):
    """
    Create Log number on save
    """
    if created and instance.log_number == "1":
        print("Signal received from Maintenance Log because created")
        log_count = MaintenanceLog.objects.filter(
            date__year=instance.date.year).count()
        print(log_count)
        log_prefix = instance.date.year
        instance.log_number = (
            str(log_prefix) + str(log_count).zfill(4))
        instance.save(update_fields=['log_number'])

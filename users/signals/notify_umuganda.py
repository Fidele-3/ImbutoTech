from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from ImbutoTech.models import ImbutoTechSession
from users.tasks.send_ImbutoTech_reminder import send_ImbutoTech_notifications


@receiver(post_save, sender=ImbutoTechSession)
def schedule_ImbutoTech_notifications(sender, instance, created, **kwargs):
   
    if created:
        
        send_ImbutoTech_notifications.delay(session_id=str(instance.id))

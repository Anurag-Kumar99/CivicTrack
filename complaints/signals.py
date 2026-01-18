from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Complaint
from .tasks import send_assignment_email_task

@receiver(post_save, sender=Complaint)
def complaint_assigned_signal(sender, instance, created, **kwargs):
    if instance.assigned_employee  and instance.status == 'PENDING':
        send_assignment_email_task.delay(
            instance.id
            # instance.assigned_employee.email
        )

@receiver(post_save, sender=Complaint)
def complaint_escalated_signal(sender, instance, **kwargs):
    if instance.status == 'ESCALATED':
        send_escalation_email_task.delay(instance.id )
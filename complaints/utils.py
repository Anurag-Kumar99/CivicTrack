from django.utils import timezone
from datetime import timedelta 
from .models import Complaint, ComplaintLog
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .emails import send_escalation_email
from complaints.models import EmployeeProfile


User = get_user_model()

def escalated_high_priority_complaints():
    deadline = timezone.now() - timedelta(days=2)

    complaints = Complaint.objects.filter(
        priority ='HIGH',
        status__in = ['PENDING', 'ACCEPTED', 'IN_PROGRESS'],
        escalated = False,
        created_at__lt = deadline
    )


    for complaint in complaints:
        complaint.escalated = True
        complaint.escalated_at = timezone.now()
        complaint.status = 'ESCALATED'
        complaint.save()
        send_escalation_email(complaint)
        log_complaint_action(
            complaint,
            action="Escalated",
            description="High priority complaint escalated after 2 days of no action"
        )

def get_least_loaded_employee(department):
    if not department:
        return None

    profiles = (
        EmployeeProfile.objects
        .filter(department=department)
        .annotate(
            pending_count=Count(
                'user__assigned_complaints',
                filter=Q(user__assigned_complaints__status='PENDING')
            )
        )
        .order_by('pending_count', 'id')  # least workload first
    )

    if profiles.exists():
        return profiles.first().user   # 👈 IMPORTANT
    return None



def log_complaint_action(complaint, action, description=""):
    ComplaintLog.objects.create(
        complaint=complaint,
        action=action,
        description=description
    )



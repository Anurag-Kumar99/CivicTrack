from django.utils import timezone
from datetime import timedelta 
from .models import Complaint, ComplaintLog
from django.db.models import Q, Count
from django.contrib.auth import get_user_model

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
        log_complaint_action(
            complaint,
            action="Escalated",
            description="High priority complaint escalated after 2 days of no action"
        )

def get_least_loaded_employee(department):
    employees = (
        User.objects.filter(role='EMPLOYEE', department=department)
        .annotate(
            pending_count=Count(
                'assigned_complaints',
                filter=Q(assigned_complaints__status='PENDING')
            )
        )
        .order_by('pending_count', 'id') #least pending first
    ) 

    return employees.first() if employees.exists() else None     


def log_complaint_action(complaint, action, description=""):
    ComplaintLog.objects.create(
        complaint=complaint,
        action=action,
        description=description
    )
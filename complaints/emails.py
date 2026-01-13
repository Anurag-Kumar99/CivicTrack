from django.core.mail import send_mail
from django.conf import settings


def send_assignment_email(employee, complaint):
    subject = "New Complaint Assigned"
    message = f"""
Hello{employee.username},

A new complaint has been assigned to you.

Title: {complaint.title}
priority: {complaint.priority}
Department: {complaint.department}

please log in to CivicTrack to take action.
""" 
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [employee.email],
        fail_silently=True
    )

def send_escalation_email(complaint):
    sunbject = " High Priority Complaint Escalated"
    message = f"""
Admin Alert,

A HIGH priority complaint has been escalated.
Title: {complaint.title}
Department: {complaint.department}
Assigned Employee: {complaint.assigned_employee}


please review immediately.

"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['admin@civictrack.com'],
        fail_silently=True
    )

    
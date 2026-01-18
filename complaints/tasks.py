from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Complaint, User


@shared_task
def send_assignment_email_task(complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    employee = complaint.assigned_employee

    print("📧 EMAIL TASK TRIGGERED")
    print("➡️ Employee:", employee.username)
    print("➡️ Email:", employee.email)

    send_mail(
        subject="New Complaint Assigned",
        message=f"""
        Hello {employee.username},

        A new complaint has been assigned to you.

        Title: {complaint.title}
        Department :{complaint.department}
        priority: {complaint.priority}
        """,

        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list=[employee.email],
    )

@shared_task
def send_escalation_email_task(complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    admins = User.objects.filter(is_superuser=True)

    for admin in admins:
        send_mail(
            subject=" Complaint Escalated ",
            message=f"""

            Admin Alert!

            A high priority complaint has been escalated.
            Title: {complaint.title}
            Department :{complaint.department}
            """,

            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin.email],
        )    
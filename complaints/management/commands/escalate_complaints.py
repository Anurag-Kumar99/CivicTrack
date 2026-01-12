from django.core.management.base import BaseCommand
from complaints.utils import escalated_high_priority_complaints

class Command(BaseCommand):
    help = 'Escalate high priority complaints that have not been addressed within the deadline'

    def handle(self, *args, **kwargs):
        escalated_high_priority_complaints()
        self.stdout.write(self.style.SUCCESS('Successfully escalated high priority complaints'))
from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model= Complaint
        fields = ['department', 'title', 'description', 'user_image']


class ResolveComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['resolved_image']   
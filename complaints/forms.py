from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model= Complaint
        fields = ['title', 'description', 'category', 'priority', 'user_image']

        widgets = {
            'title' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter complaint title'
            }),
            'description' : forms.TextInput(attrs={
                'class' : 'form-control',
                'rows' : 4,
                'placeholder' : 'Describe your complaint here'
            }),
            'category' : forms.Select(attrs={
                'class' : 'form-select',
            }),
            'priority' : forms.Select(attrs={
                'class' : 'form-select',
            })
           
        }


class ResolveComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'priority', 'resolved_image', 'department']   
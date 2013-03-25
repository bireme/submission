from django import forms
from models import *

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ('created', 'updated', 'creator', 'updater', 'current_status')

class SubmissionIsoForm(forms.ModelForm):
    class Meta:
        model = TypeSubmission
        fields = ('total_records', 'bibliographic_type' ,'iso_file', 'observation', 'file', 'external', 'txt_external')
        widgets = {
            'total_records': forms.TextInput(attrs={'class': 'span1'}),
        }

class SubmissionIsoFinalForm(forms.ModelForm):
    class Meta:
        model = TypeSubmission
        exclude = ('created', 'updated', 'creator', 'updater', 'submission', 'iso_file')

class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        exclude = ('created', 'updated', 'creator', 'updater', 'submission', 'previous_status', 'current_status')


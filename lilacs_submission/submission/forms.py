from django import forms
from models import *

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ('created', 'updated', 'creator', 'updater', 'current_status')

class SubmissionIsoForm(forms.ModelForm):
    class Meta:
        model = TypeSubmission
        fields = ('total_records', 'type' ,'iso_file')

class SubmissionIsoFinalForm(forms.ModelForm):
    class Meta:
        model = TypeSubmission
        fields = ('total_records', 'certified')

class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        exclude = ('created', 'updated', 'creator', 'updater', 'submission', 'previous_status', 'current_status')


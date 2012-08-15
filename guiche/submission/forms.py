from django import forms
from models import *

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ('created', 'updated', 'creator', 'updater', 'status')

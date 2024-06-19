# forms.py

from django import forms

class MessageForm(forms.Form):
    recipient_id = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea)

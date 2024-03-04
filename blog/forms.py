from django import forms

class ConversationForm(forms.Form):

    prompt = forms.CharField(widget=forms.Textarea, label='prompt', min_length=2)
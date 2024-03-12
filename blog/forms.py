
from .models import BlogRequestModel
from django import forms
from django.forms import Textarea, CharField

class BlogRequestForm(forms.ModelForm):

    class Meta:
        model = BlogRequestModel
        exclude = ["user","ts","status"]
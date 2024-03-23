
from .models import BlogRequestModel
from django import forms

class BlogRequestForm(forms.ModelForm):

    class Meta:
        model = BlogRequestModel
        exclude = ["user","ts","status","blogurl", "imgurl"]
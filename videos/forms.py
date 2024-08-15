
from .models import VideoRequestModel
from django import forms

class VideoRequestForm(forms.ModelForm):

    class Meta:
        model = VideoRequestModel
        exclude = ["user","ts","status","videourl", "imgurl"]
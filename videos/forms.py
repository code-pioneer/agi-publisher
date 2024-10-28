
from .models import VideoRequestModel, VideoTaskModel
from django import forms

class VideoRequestForm(forms.ModelForm):

    class Meta:
        model = VideoRequestModel
        exclude = ["user","ts","status","videourl", "imgurl", "video_name", "transcript", "voice", "image_prompt"]

class VideoTaskForm(forms.ModelForm):

    class Meta:
        model = VideoTaskModel
        exclude = ["ts","status", "video_id"]

        
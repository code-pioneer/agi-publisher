from django.db import models
import uuid

class VideoRequestModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=500, default='')
    status = models.CharField(max_length=40, default='')
    videourl = models.CharField(max_length=255, null=True)
    imgurl = models.CharField(max_length=255, null=True)
    user = models.CharField(max_length=40, default='')
    ts = models.DateTimeField(auto_now=True)
    seo_checkbox = models.BooleanField(default=False)
    in_depth_checkbox = models.BooleanField(default=False)
    theme_choices = [
        ('descriptive', 'Descriptive'),
        ('expository', 'Expository'),        
        ('humor', 'Humor'),
        ('informative', 'Informative'),
        ('narrative', 'Narrative'),
        ('persuasive', 'Persuasive')
    ]
    theme = models.CharField(max_length=20, null=True, choices=theme_choices, default='descriptive')
    
    def get_related_video_response(self):
        video_response_model = VideoResponseModel.objects.filter(video_id=self).order_by('-created_ts')
        return video_response_model


class VideoResponseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_id = models.ForeignKey(VideoRequestModel, on_delete=models.CASCADE)
    video_entries = models.JSONField(default=dict)
    ts = models.DateTimeField(auto_now=True)
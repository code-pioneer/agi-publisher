from django.db import models
import uuid

class BlogRequestModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=500, default='')
    status = models.CharField(max_length=40, default='')
    blogurl = models.CharField(max_length=255, null=True)
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
    
    def get_related_blog_response(self):
        blog_response_model = BlogResponseModel.objects.filter(blog_id=self).order_by('-created_ts')
        return blog_response_model


class BlogResponseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog_id = models.ForeignKey(BlogRequestModel, on_delete=models.CASCADE)
    blog_entries = models.JSONField(default=dict)
    ts = models.DateTimeField(auto_now=True)
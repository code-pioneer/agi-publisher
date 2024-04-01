from django.db import models
import uuid

class BlogRequestModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=120, default='')
    status = models.CharField(max_length=40, default='')
    blogurl = models.CharField(max_length=255, null=True)
    imgurl = models.CharField(max_length=255, null=True)
    user = models.CharField(max_length=40, default='')
    ts = models.DateTimeField(auto_now=True)

    def get_related_blog_response(self):
        blog_response_model = BlogResponseModel.objects.filter(blog_id=self).order_by('-created_ts')
        return blog_response_model


class BlogResponseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog_id = models.ForeignKey(BlogRequestModel, on_delete=models.CASCADE)
    blog_entries = models.JSONField(default=dict)
    ts = models.DateTimeField(auto_now=True)
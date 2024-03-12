from .models import BlogRequestModel, BlogResponseModel
from .models import BlogRequestModel, BlogResponseModel

def get_all_blogs():
    try:
        return BlogRequestModel.objects.select_related('blogresponsemodel').all()
    except BlogRequestModel.DoesNotExist:
        return None

# Rest of the code remains the same...
def get_blog_by_id(id):
    try:
        return BlogRequestModel.objects.get(pk=id)
    except BlogRequestModel.DoesNotExist:
        return None
    
def get_blog_by_user(user):
    try:
        return BlogRequestModel.objects.filter(user=user)
    except BlogRequestModel.DoesNotExist:
        return None

def get_blog_by_status(status):
    try:
        return BlogRequestModel.objects.filter(status=status)
    except BlogRequestModel.DoesNotExist:
        return None
    
def save_blog_request(topic, status, user):
    try:
        blog_request = BlogRequestModel(topic=topic, status=status, user=user)
        print("save_blog_request: ", blog_request)
        blog_request.save()
        print("Blog Request ID: ", blog_request.id)
        return blog_request
    except Exception as e:
        print("An error occured in save_blog_request", e)
        return None
    
def save_blog_response(blog_id, blog_entries):
    try:
        blog_response = BlogResponseModel(blog_id=blog_id, blog_entries=blog_entries)
        blog_response.save()
        return blog_response
    except Exception as e:
        print("An error occured in save_blog_response", e)
        return None
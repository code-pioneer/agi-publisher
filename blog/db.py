from .models import BlogRequestModel, BlogResponseModel
from .models import BlogRequestModel, BlogResponseModel
from asgiref.sync import async_to_sync, sync_to_async

async def get_all_blogs():
    try:
        return await sync_to_async(BlogRequestModel.objects.select_related('blogresponsemodel').all)()
    except BlogRequestModel.DoesNotExist:
        return None

# Rest of the code remains the same...
async def get_blog_by_id(id):
    try:
        return await sync_to_async(BlogRequestModel.objects.get)(pk=id)
    except BlogRequestModel.DoesNotExist:
        return None
    
async def get_blog_by_user(user):
    try:
        return await sync_to_async(BlogRequestModel.objects.filter)(user=user)
    except BlogRequestModel.DoesNotExist:
        return None

async def get_blog_by_status(status):
    try:
        return await sync_to_async(BlogRequestModel.objects.filter)(status=status)
    except BlogRequestModel.DoesNotExist:
        return None
    
async def save_blog_request(topic, status, user):
    try:
        create_blog_request = sync_to_async(BlogRequestModel.objects.create)
        
        blog_request_instance = await create_blog_request(
            topic=topic,
            status=status,
            user=user
        )
        print("save_blog_request: ", blog_request_instance)
        return blog_request_instance
    except Exception as e:
        print("An error occured in save_blog_request", e)
        return None
    
async def save_blog_response(blog_id, blog_entries):
        try:
            create_blog_response = sync_to_async(BlogResponseModel.objects.create)
            
            blog_response_instance = await create_blog_response(
                blog_id=blog_id,
                blog_entries=blog_entries
            )
            print("save_blog_response: ", blog_response_instance)
            return blog_response_instance
        except Exception as e:
            print("An error occurred in save_blog_response", e)
            return None
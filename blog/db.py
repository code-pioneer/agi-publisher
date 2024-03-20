from .models import BlogRequestModel, BlogResponseModel
from .models import BlogRequestModel, BlogResponseModel
from asgiref.sync import sync_to_async

async def get_all_blogs():
    try:
        return await sync_to_async(BlogRequestModel.objects.select_related('blogresponsemodel').all)()
    except BlogRequestModel.DoesNotExist:
        return None

async def get_blog_by_id(id):
    try:
        return await sync_to_async(BlogRequestModel.objects.get)(pk=id)
    except BlogRequestModel.DoesNotExist:
        return None
    
async def get_blog_by_user(user):
    try:
        @sync_to_async
        def get_blog_response(user):
            return list(BlogRequestModel.objects.filter(user=user))

        queryset = await get_blog_response(user)   
        blog_list = [blog.id.hex for blog in queryset]
        return list(blog_list)
    except BlogRequestModel.DoesNotExist:
        return None
   
async def get_blog_by_status(status):
    try:
        @sync_to_async
        def get_blog_response(status):
            return list(BlogRequestModel.objects.filter(status=status))

        queryset = await get_blog_response(status)   
        blog_list = [blog.id.hex for blog in queryset]
        return list(blog_list)
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
        # print("save_blog_response: ", blog_response_instance)
        return blog_response_instance
    except Exception as e:
        print("An error occurred in save_blog_response", e)
        return None
       
async def get_blog_response_by_request_id(request_id):
    try:
        @sync_to_async
        def get_blog_response(request_id):
            return list(BlogResponseModel.objects.filter(blog_id=request_id).order_by('ts'))

        queryset = await get_blog_response(request_id)   
        blog_list = [blog.blog_entries for blog in queryset]
        return list(blog_list)
    except BlogResponseModel.DoesNotExist:
        return None
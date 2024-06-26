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
            return list(BlogRequestModel.objects.filter(user=user, status='published'))

        queryset = await get_blog_response(user)       
        blog_list = []
        for blog in queryset:
            blog_data = {
                'id': blog.id.hex,
                'url': blog.blogurl,
                'imgurl': blog.imgurl,
                'topic': blog.topic,
                'status': blog.status,
                'seo_checkbox': blog.seo_checkbox,
                'in_depth_checkbox': blog.in_depth_checkbox,
                'ts': blog.ts,
            }
            blog_list.append(blog_data)
        return blog_list
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
    
async def save_blog_request(topic, status, user, blogurl=None, imgurl=None, seo_checkbox=False, in_depth_checkbox=False, theme='descriptive'):
    try:
        create_blog_request = sync_to_async(BlogRequestModel.objects.create)
        
        blog_request_instance = await create_blog_request(
            topic=topic,
            status=status,
            user=user,
            blogurl=blogurl,
            imgurl=imgurl,
            seo_checkbox=seo_checkbox,
            in_depth_checkbox=in_depth_checkbox,
            theme=theme
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
       
async def get_blog_response_by_request_id(request_id, since_ts):
    try:
        @sync_to_async
        def get_blog_response(request_id, since_ts):
            return list(BlogResponseModel.objects.filter(blog_id=request_id, ts__gt=since_ts).order_by('ts'))

        queryset = await get_blog_response(request_id, since_ts)   
        blog_list = [blog.blog_entries for blog in queryset]
        return blog_list, (queryset[-1].ts if queryset else since_ts)
    except BlogResponseModel.DoesNotExist:
        return [], since_ts


    
async def update_blog_request(request_id, status='awaiting', blogurl=None, imgurl=None, topic=None):
    try:
        blog_request_instance = await sync_to_async(BlogRequestModel.objects.get)(pk=request_id)
        blog_request_instance.status = status
        if blogurl:
            blog_request_instance.blogurl = blogurl
        if imgurl:
            blog_request_instance.imgurl = imgurl
        if topic:
            blog_request_instance.topic = topic
        await sync_to_async(blog_request_instance.save)()
        return blog_request_instance
    except BlogRequestModel.DoesNotExist:
        return None

async def get_blog_entries_by_id(id):
    try:
        return await sync_to_async(
            BlogResponseModel.objects.filter(blog_id_id=id, 
                                             blog_entries__event='output',
                                             blog_entries__profile__name='Influencer').values('blog_entries__messageData').get)()
    except BlogResponseModel.DoesNotExist:
        return None
    
async def delete_blog_request(id):
    try:
        blog_request_instance = await sync_to_async(BlogRequestModel.objects.get)(pk=id)
        await sync_to_async(blog_request_instance.delete)()
        return True
    except BlogRequestModel.DoesNotExist:
        return False
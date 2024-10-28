from .models import VideoRequestModel, VideoResponseModel, VideoTaskModel
from asgiref.sync import sync_to_async

async def get_task_by_id(id):
    try:
        return await sync_to_async(VideoTaskModel.objects.get)(pk=id)
    except VideoTaskModel.DoesNotExist:
        return None

# Define the synchronous function for filtering
def filter_task_sync(id):
    return VideoTaskModel.objects.filter(pk=id).first()  # Use `.first()` to get the first match or None

async def get_task_by_id(id):
    # Call the synchronous function in the async context
    task = await sync_to_async(filter_task_sync)(id)
    return task 
    
async def save_video_task(video_id, task_name, status):
    try:
        create_video_task = sync_to_async(VideoTaskModel.objects.create)
            
        video_task_instance = await create_video_task(
            video_id=video_id,
            task_name=task_name,
            status=status
        )
        # print("save_video_response: ", video_response_instance)
        return video_task_instance
    except Exception as e:
        print("An error occurred in save_video_task", e)
        return None
    
async def update_video_task(id, status='complete'):
    try:
        video_task_instance = await sync_to_async(VideoTaskModel.objects.get)(pk=id)
        video_task_instance.status = status

        await sync_to_async(video_task_instance.save)()
        return video_task_instance
    except VideoTaskModel.DoesNotExist:
        return None
    
async def get_all_videos():
    try:
        return await sync_to_async(VideoRequestModel.objects.select_related('blogresponsemodel').all)()
    except VideoRequestModel.DoesNotExist:
        return None

async def get_video_by_id(id):
    try:
        return await sync_to_async(VideoRequestModel.objects.get)(pk=id)
    except VideoRequestModel.DoesNotExist:
        return None
    
async def get_video_by_user(user):
    try:
        @sync_to_async
        def get_video_response(user):
            return list(VideoRequestModel.objects.filter(user=user, status='published'))

        queryset = await get_video_response(user)       
        video_list = []
        for video in queryset:
            video_data = {
                'id': video.id.hex,
                'url': video.videourl,
                'imgurl': video.imgurl,
                'topic': video.topic,
                'status': video.status,
                'long_video': video.long_video,
                'ts': video.ts,
            }
            video_list.append(video_data)
        return video_list
    except VideoRequestModel.DoesNotExist:
        return None
   
async def get_video_by_status(status):
    try:
        @sync_to_async
        def get_video_response(status):
            return list(VideoRequestModel.objects.filter(status=status))

        queryset = await get_video_response(status)   
        video_list = [video.id.hex for video in queryset]
        return list(video_list)
    except VideoRequestModel.DoesNotExist:
        return None
    
async def save_video_request(topic, status, user, videourl=None, imgurl=None, long_video=False, theme='build', video_name=None, transcript=None, voice=None, image_prompt=None):
    try:
        create_video_request = sync_to_async(VideoRequestModel.objects.create)
        
        video_request_instance = await create_video_request(
            topic=topic,
            status=status,
            user=user,
            videourl=videourl,
            imgurl=imgurl,
            long_video=long_video,
            theme=theme,
            video_name=video_name,
            transcript=transcript,
            voice=voice,
            image_prompt=image_prompt
        )
        print("save_video_request: ", video_request_instance)
        return video_request_instance
    except Exception as e:
        print("An error occured in save_video_request", e)
        return None
    
async def save_video_response(video_id, video_entries):
    try:
        create_video_response = sync_to_async(VideoResponseModel.objects.create)
            
        video_response_instance = await create_video_response(
            video_id=video_id,
            video_entries=video_entries
        )
        # print("save_video_response: ", video_response_instance)
        return video_response_instance
    except Exception as e:
        print("An error occurred in save_video_response", e)
        return None
       
async def get_video_response_by_request_id(request_id, since_ts):
    try:
        @sync_to_async
        def get_video_response(request_id, since_ts):
            return list(VideoResponseModel.objects.filter(video_id=request_id, ts__gt=since_ts).order_by('ts'))

        queryset = await get_video_response(request_id, since_ts)   
        video_list = [video.video_entries for video in queryset]
        return video_list, (queryset[-1].ts if queryset else since_ts)
    except VideoResponseModel.DoesNotExist:
        return [], since_ts

    
async def update_video_request(request_id, status='awaiting', videourl=None, imgurl=None, topic=None, video_name=None, transcript=None, long_video=False, voice=None, image_prompt=None):
    try:
        video_request_instance = await sync_to_async(VideoRequestModel.objects.get)(pk=request_id)
        video_request_instance.status = status
        if videourl:
            video_request_instance.videourl = videourl
        if imgurl:
            video_request_instance.imgurl = imgurl
        if topic:
            video_request_instance.topic = topic
        if video_name:
            video_request_instance.video_name = video_name
        if transcript:
            video_request_instance.transcript = transcript
        if long_video:
            video_request_instance.long_video = long_video
        if voice:
            video_request_instance.voice = voice
        if image_prompt:
            video_request_instance.image_prompt = image_prompt
            
        await sync_to_async(video_request_instance.save)()
        return video_request_instance
    except VideoRequestModel.DoesNotExist:
        return None

async def get_video_entries_by_id(id):
    try:
        return await sync_to_async(
            VideoResponseModel.objects.filter(video_id_id=id, 
                                             video_entries__event='output',
                                             video_entries__profile__name='Influencer').values('video_entries__messageData').get)()
    except VideoResponseModel.DoesNotExist:
        return None
    
async def delete_video_request(id):
    try:
        video_request_instance = await sync_to_async(VideoRequestModel.objects.get)(pk=id)
        await sync_to_async(video_request_instance.delete)()
        return True
    except VideoRequestModel.DoesNotExist:
        return False
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST, require_GET
from asgiref.sync import sync_to_async
from .forms import VideoRequestForm
from home import menu
from .db import save_video_request, get_video_by_user, get_video_by_id,get_video_entries_by_id, delete_video_request
from videos.agi_agent import video_agent
import asyncio


team_template = 'videoteam.html'
video_template   = 'video_create.html'
myvideos_template = 'myvideos.html'
social_content_template= 'videosocialcontent.html'
playvideo_template = 'playvideo.html'

    
@require_GET
async def get_team(request):
    print("view get_team")
    try:
        items = menu.get_navbar('Videos Team')
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        return render(request, team_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')

@require_GET
async def get_create_videos(request):
    print("view get_create_videos")
    try:
        items = menu.get_navbar('Create Videos')
        items['form'] = VideoRequestForm()
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        return render(request, video_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_GET
async def myvideos(request):
    print("view myvideos")
    try:
        items = menu.get_navbar('My Videos')
        items['form'] = VideoRequestForm()
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        async_get_username = sync_to_async(lambda: request.user.username)  
        username = await async_get_username()
        items['videos'] = await get_video_by_user(user=username)
        print("items['videos']: ", items['videos'])
        return render(request, myvideos_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_GET
async def playvideo(request, id):
    print("playvideo")
    try:
        items = menu.get_navbar('My Videos')
        items['form'] = VideoRequestForm()
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        async_get_username = sync_to_async(lambda: request.user.username)  
        items['video'] = await get_video_by_id(id=id)
        print("items['video']: ", items['video'])
        return render(request, playvideo_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_POST
async def create(request):
    print("view create")
    form = VideoRequestForm(request.POST)
    print('form ', request.POST)
    print('form ', form)

    try:
        if form.is_valid():            
            topic = request.POST.get("topic")
            theme = request.POST.get("theme")
            in_depth_checkbox = request.POST.get('in_depth_checkbox') == 'true'
            seo_checkbox = request.POST.get('seo_checkbox') == 'true'              
            async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
            user_is_authenticated = await async_get_is_authenticated()
            if not user_is_authenticated:
                return redirect('/accounts/login/')
            async_get_username = sync_to_async(lambda: request.user.username)    
            username = await async_get_username()
            video_instance = await save_video_request(topic, status='awaiting', user=username, seo_checkbox=seo_checkbox, in_depth_checkbox=in_depth_checkbox, theme=theme)
            asyncio.create_task(video_agent(topic, video_instance.id))
            return JsonResponse({'message': 'Task triggered successfully', 'id': video_instance.id})
        else:
            message = {'answer': '''Apologies, I am not equipped to handle this particular task. Please consider another query or topic for assistance.'''}
            return JsonResponse(message)
    except Exception as e:
        print("An error occured in chat post view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')

@require_GET
async def retrieve_by_id(request, id):
    print("view retrieve_by_id")
    try:
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')

        video = await get_video_by_id(id=id)
        file_path = video.videourl
        file_extension = file_path.split('.')[-1]
        if file_extension == 'md':
            with open(file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
                response = HttpResponse(md_content, content_type='text/markdown')
                response['Content-Disposition'] = 'inline; filename="file.md"'
        elif file_extension == 'html':
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                response = HttpResponse(html_content, content_type='text/html')
                response['Content-Disposition'] = 'inline; filename="file.html"'
        elif file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                txt_content = f.read()
                response = HttpResponse(txt_content, content_type='text/plain')
                response['Content-Disposition'] = 'inline; filename="file.txt"'
        elif file_extension == 'mp4':
            with open(file_path, 'rb') as video_file:
                response = HttpResponse(video_file.read(), content_type="video/mp4")
                response['Content-Disposition'] = 'attachment; filename="processed_video.mp4"'
                return response
        else:
            return HttpResponseServerError('Invalid file type')
        return response
    except Exception as e:
        print("An error occured in chat post view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
 
@require_GET
async def retrieve_socials_by_id(request, id):
    print("view retrieve_socials_by_id")
    try:
        items = menu.get_navbar('My Videos')
        items['form'] = VideoRequestForm()
        
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')

        social_content = await get_video_entries_by_id(id=id)
        content_list = social_content['video_entries__messageData'].split("\n\n")
        tweet_list = []
        for i in range(len(content_list)):
            parts_dict = {}
            if not content_list[i].startswith('Answer:') and not content_list[i].startswith('('):
                parts = content_list[i].split('#')
                for i in range(len(parts)):
                    if i == 0:
                        parts_dict["details"] = parts[i]
                    else:
                        parts_dict["hashtags"] = ['#' + part.strip() for part in parts[i:] if part.strip()]  
                        break
                tweet_list.append(parts_dict)            
        items['content_list'] =tweet_list
        
        video = await get_video_by_id(id=id)
        items['video']= video
        return render(request, social_content_template, items)
    except Exception as e:
        print("An error occured in retrieve_entries_by_id view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    

@require_GET
async def delete_by_id(request, id):
    print("view retrieve_by_id")
    try:
        items = menu.get_navbar('My Videos')
        items['form'] = VideoRequestForm()
        
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')

        await delete_video_request(id=id)
        return redirect('/video/myvideos/')

        
    except Exception as e:
        print("An error occured in retrieve_entries_by_id view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
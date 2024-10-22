from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from asgiref.sync import sync_to_async
from .forms import VideoRequestForm, VideoTaskForm
from home import menu
from .db import save_video_request, get_video_by_user, get_video_by_id,get_video_entries_by_id, delete_video_request, save_video_task, update_video_request
from videos.agi_agent import video_agent
import asyncio
from . agis.themes import themes
from . agis.tasks import tasks

team_template = 'videoteam.html'
video_template   = 'video_create.html'
myvideos_template = 'myvideos.html'
social_content_template= 'videosocialcontent.html'
playvideo_template = 'playvideo.html'
themes_template = 'themes.html'


    
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
async def get_themes(request):
    print("view get_themes")
    try:
        items = menu.get_navbar('Create Videos')
        items['form'] = VideoRequestForm()
        items['themes'] = themes
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        return render(request, themes_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_POST
async def save_theme(request):
    print("view save_theme")

    try:
        
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        
        selected_theme = request.POST.get('theme_id')
        valid_themes = [theme['theme_id'] for theme in themes]

        if selected_theme not in valid_themes:
            return HttpResponseBadRequest("Invalid theme selection")
   
        async_get_username = sync_to_async(lambda: request.user.username)  

        username = await async_get_username()
        
        if selected_theme == 'build':
            video_instance = await save_video_request(topic='', status='awaiting', user=username, long_video=False, theme=selected_theme)

            task_name = tasks[0]
            return redirect('select_task', selection_type='current', video_id=video_instance.id, task_name=task_name)
        else:
            return redirect('select_topic', theme_id=selected_theme)
    except Exception as e:
        print("An error occured in chat post view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')

@require_GET
async def select_topic(request, theme_id):
    print("view select_topic")
    try:
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        
        items = menu.get_navbar('Create Videos')
        items['form'] = VideoRequestForm()
        selected_theme = next((theme for theme in themes if theme['theme_id'] == theme_id), None)
        items['selected_theme'] = selected_theme

        return render(request, video_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_GET
async def select_task(request,selection_type, video_id, task_name):
    print("view select_task")
    try:

        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
    
        items = menu.get_navbar('Create Videos')
        items['form'] = VideoRequestForm()
        
        video_instance = await get_video_by_id(id=video_id)
        items['video'] = video_instance

        selected_theme = next((theme for theme in themes if theme['theme_id'] == video_instance.theme), None)
        items['selected_theme'] = selected_theme
        if task_name in tasks:
            current_task_index = tasks.index(task_name)
            if selection_type == 'next':                    
                # Check if there is a next item in the list
                if current_task_index + 1 < len(tasks):
                    task_name = tasks[current_task_index + 1]
                    current_task_index = current_task_index + 1
                else:
                    return render(request, '404.html')  # Handle invalid step

        else:
            return render(request, '404.html')  # Handle invalid step

        items['task_name'] = task_name

        # Pass the current step and all steps to the template
        context = {
            'current_task': task_name,
            'tasks': tasks,
            'past_tasks': tasks[:current_task_index],    # Past steps
            'future_tasks': tasks[current_task_index+1:], # Future steps
        }
        items['context'] = context
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
        return render(request, playvideo_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_POST
async def create(request):
    print("view create")
    form = VideoRequestForm(request.POST)
    try:
        if form.is_valid():            
            topic = request.POST.get("topic")
            theme_id = request.POST.get("theme")
            long_video = request.POST.get('long_video') == 'true'
            async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
            user_is_authenticated = await async_get_is_authenticated()
            if not user_is_authenticated:
                return redirect('/accounts/login/')
            async_get_username = sync_to_async(lambda: request.user.username)    
            username = await async_get_username()
            video_instance = await save_video_request(topic, status='awaiting', user=username, long_video=long_video, theme=theme_id)
            interactive_mode = False
            task_name=None
            task_id=None
            asyncio.create_task(video_agent(topic=topic,id=video_instance.id, interactive_mode=interactive_mode,task_name=task_name, task_id=task_id))

            return JsonResponse({'message': 'Task triggered successfully', 'id': video_instance.id})
        else:
            message = {'answer': '''Apologies, I am not equipped to handle this particular task. Please consider another query or topic for assistance.'''}
            return JsonResponse(message)
    except Exception as e:
        print("An error occured in chat post view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')

@require_POST
async def process_task(request):
    print("view process_task")
    
    post_data = request.POST.copy()
    if 'video_id' in post_data:
        del post_data['video_id']

    form = VideoTaskForm(post_data)

    try:
        if form.is_valid():            
            task_name = request.POST.get("task_name")
            video_id = request.POST.get("video_id")
            topic = request.POST.get("topic")
            long_video = request.POST.get('long_video') == 'true'

            async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
            user_is_authenticated = await async_get_is_authenticated()
            if not user_is_authenticated:
                return redirect('/accounts/login/')
            
            video_instance = await get_video_by_id(id=video_id)
            if task_name == 'transcript':
                video_instance = await update_video_request(request_id=video_id, topic=topic, long_video=long_video)
            else:
                video_instance = await get_video_by_id(id=video_id)

            interactive_mode = True
            if task_name in tasks:
                video_task_instance = await save_video_task(video_id=video_instance, task_name=task_name, status='pending')
                task_id = video_task_instance.id
  
                asyncio.create_task(video_agent(topic=video_instance.topic,id=video_instance.id, interactive_mode=interactive_mode,task_name=task_name, task_id=task_id))
                return JsonResponse({'message': 'Task triggered successfully', 'id': video_instance.id, 'task_id': task_id})
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
    
from django.shortcuts import render

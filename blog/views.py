import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST, require_GET
from asgiref.sync import sync_to_async
from .forms import BlogRequestForm
from home import menu
from .db import save_blog_request, get_blog_by_user, get_blog_by_id,get_blog_entries_by_id, delete_blog_request
from blog.agi_agent import blog_agent
import asyncio


team_template = 'team.html'
blog_template   = 'create.html'
myblogs_template = 'myblogs.html'
social_content_template= 'socialcontent.html'
    
@require_GET
async def get_team(request):
    print("view get_team")
    try:
        items = menu.get_navbar('Team')
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        return render(request, team_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')

@require_GET
async def get_create_blogs(request):
    print("view get_user_blogs")
    try:
        items = menu.get_navbar('Create')
        items['form'] = BlogRequestForm()
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        return render(request, blog_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_GET
async def myblogs(request):
    print("view myblogs")
    try:
        items = menu.get_navbar('My Articles')
        items['form'] = BlogRequestForm()
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        async_get_username = sync_to_async(lambda: request.user.username)  
        username = await async_get_username()
        items['blogs'] = await get_blog_by_user(user=username)
        print("items['blogs']: ", items['blogs'])
        return render(request, myblogs_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_POST
async def create(request):
    print("view create")
    form = BlogRequestForm(request.POST)
    try:
        if form.is_valid():
            topic = request.POST.get("topic")
            theme = request.POST.get("theme")

            if 'in_depth_checkbox' in request.POST:
                in_depth_checkbox = True
            else:
                in_depth_checkbox = False
            if 'seo_checkbox' in request.POST:
                seo_checkbox = True
            else:
                seo_checkbox = False                

            async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
            user_is_authenticated = await async_get_is_authenticated()
            if not user_is_authenticated:
                return redirect('/accounts/login/')
            async_get_username = sync_to_async(lambda: request.user.username)    
            username = await async_get_username()
            blog_instance = await save_blog_request(topic, status='awaiting', user=username, seo_checkbox=seo_checkbox, in_depth_checkbox=in_depth_checkbox, theme=theme)
            asyncio.create_task(blog_agent(topic, blog_instance.id))
            return JsonResponse({'message': 'Task triggered successfully', 'id': blog_instance.id})
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

        blog = await get_blog_by_id(id=id)
        file_path = blog.blogurl
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
        else:
            return HttpResponseServerError('Invalid file type')
        return response
    except Exception as e:
        print("An error occured in chat post view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
 
@require_GET
async def retrieve_entries_by_id(request, id):
    print("view retrieve_entries_by_id")
    try:
        items = menu.get_navbar('My Articles')
        items['form'] = BlogRequestForm()
        
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')

        social_content = await get_blog_entries_by_id(id=id)
        content_list = social_content['blog_entries__messageData'].split("\n\n")
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
        
        blog = await get_blog_by_id(id=id)
        items['blog']= blog
        return render(request, social_content_template, items)
    except Exception as e:
        print("An error occured in retrieve_entries_by_id view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    

@require_GET
async def delete_by_id(request, id):
    print("view retrieve_by_id")
    try:
        items = menu.get_navbar('My Articles')
        items['form'] = BlogRequestForm()
        
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')

        await delete_blog_request(id=id)
        return redirect('/blog/myblogs/')

        
    except Exception as e:
        print("An error occured in retrieve_entries_by_id view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST, require_GET
from asgiref.sync import sync_to_async
from .forms import BlogRequestForm
from home import menu
from .db import save_blog_request, get_blog_by_user



blog_template   = 'blog.html'

@require_GET
def get_blogs(request):
    print("view get_blogs")
    try:
        items = menu.get_navbar('Blog')
        items['form'] = BlogRequestForm()
        return render(request, blog_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@require_GET
async def get_user_blogs(request):
    print("view get_user_blogs")
    try:
        items = menu.get_navbar('Blog')
        items['form'] = BlogRequestForm()
        async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
        user_is_authenticated = await async_get_is_authenticated()
        if not user_is_authenticated:
            return redirect('/accounts/login/')
        async_get_username = sync_to_async(lambda: request.user.username)  
        username = await async_get_username()
        items['blogs'] = await get_blog_by_user(user=username)
        return render(request, blog_template, items)
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
            async_get_is_authenticated = sync_to_async(lambda: request.user.is_authenticated)  
            user_is_authenticated = await async_get_is_authenticated()
            if not user_is_authenticated:
                return redirect('/accounts/login/')
            async_get_username = sync_to_async(lambda: request.user.username)    
            username = await async_get_username()
            blog_instance = await save_blog_request(topic, status='awaiting', user=username)
            print("blog_instance: ", blog_instance)
            return JsonResponse({'message': 'Task triggered successfully', 'id': blog_instance.id})
        else:
            message = {'answer': '''Apologies, I am not equipped to handle this particular task. Please consider another query or topic for assistance.'''}
            return JsonResponse(message)
    except Exception as e:
        print("An error occured in chat post view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')

@login_required
@require_POST
async def retrieve(request):
 pass
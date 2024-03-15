from channels.layers import get_channel_layer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST, require_GET
import markdown
from .forms import BlogRequestForm
from home import menu
from .db import save_blog_request, get_blog_by_user, get_all_blogs
from mainapp.settings import BLOG_CREATE_CHANNEL_NAME



blog_template   = 'blog.html'

@login_required
@require_GET
def get_blogs(request):
    try:
        items = menu.get_navbar('Blog')
        items['form'] = BlogRequestForm()
        items['blogs'] = get_all_blogs()
        return render(request, blog_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@login_required
@require_GET
async def get_user_blogs(request):

    try:
        items = menu.get_navbar('Blog')
        items['form'] = BlogRequestForm()
        items['blogs'] = await get_blog_by_user(user=request.user.username)
        return render(request, blog_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@login_required
@require_POST
async def create(request):
    form = BlogRequestForm(request.POST)
    try:
        if form.is_valid():
            topic = request.POST.get("topic")
            blog_instance = await save_blog_request(topic, status='awaiting', user=request.user.username)
            data = {
                 'id': str(blog_instance.id),
                 'topic': topic,
            }
            channel_layer = get_channel_layer()
            await channel_layer.send(BLOG_CREATE_CHANNEL_NAME, {'type': 'task.start', 'data': data})

            return JsonResponse({'message': 'Task triggered successfully', 'id': str(blog_instance.id)})
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
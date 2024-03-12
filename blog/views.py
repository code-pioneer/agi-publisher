from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
import markdown
from .forms import BlogRequestForm
from home import menu
from django.views.decorators.http import require_POST, require_GET
from .db import save_blog_request, get_blog_by_user, get_all_blogs, save_blog_response


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
def get_user_blogs(request):
    try:
        items = menu.get_navbar('Blog')
        items['form'] = BlogRequestForm()
        items['blogs'] = get_blog_by_user(user=request.user.username)
        return render(request, blog_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
@login_required
@require_POST
def create(request):
    form = BlogRequestForm(request.POST)
    try:
        if form.is_valid():
            topic = request.POST.get("topic")
            blog_instance = save_blog_request(topic, status='PENDING', user=request.user.username)
            blog_id = blog_instance.id
            print("Blog ID: ", blog_id)
            data = {'answer': blog_id}   
            # Add code to initiate the task to create Blog using agi_agent.blog_agent
            return JsonResponse(data)
        else:
            message = {'answer': '''Apologies, I am not equipped to handle this particular task. Please consider another query or topic for assistance.'''}
            return JsonResponse(message)
    except Exception as e:
        print("An error occured in chat post view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')

# @login_required
@require_POST
async def retrieve(request):
 pass
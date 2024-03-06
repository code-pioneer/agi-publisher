from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
import markdown
from .forms import ConversationForm
from home import menu
from . import agi_agent 

blog_template   = 'blog.html'

# @login_required
def chat_get(request):
    try:
        items = menu.get_navbar('Blog')
        items['form'] = ConversationForm()
        return render(request, blog_template, items)
    except Exception as e:
        print("An error occured in chat view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
    
# @login_required
def chat_post(request):
    form = ConversationForm(request.POST)
    try:
        if form.is_valid():
            prompt = request.POST.get("prompt")
            resp_dict = agi_agent.blogAgent(topic=prompt) 
            answer =  resp_dict['answer'] 
            md = markdown.Markdown(extensions=["fenced_code"])
            html = md.convert(answer)
            data = {'answer': html}               
            return JsonResponse(data)
        else:
            message = {'answer': '''Apologies, I am not equipped to handle this particular task. Please consider another query or topic for assistance.'''}
            return JsonResponse(message)
    except Exception as e:
        print("An error occured in chat post view", e)
        return HttpResponseServerError('Humm... Something went wrong... Try later')
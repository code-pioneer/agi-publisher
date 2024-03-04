from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_get, name= "chat"),
    path('post', views.chat_post, name = "chat_prompt"),
]
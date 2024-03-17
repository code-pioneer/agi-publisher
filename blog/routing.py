from django.urls import re_path

from .consumers import create_consumer, retrieve_consumer

websocket_urlpatterns = [
    re_path(r'ws/retrieve/$', retrieve_consumer.RetrieveBlogConsumer.as_asgi()), 
    re_path(r'ws/create/$', create_consumer.CreateBlogConsumer.as_asgi()),    
   
]
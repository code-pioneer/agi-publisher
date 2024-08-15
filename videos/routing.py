from django.urls import re_path

from .consumers import retrieve_consumer

websocket_urlpatterns = [
    re_path(r'ws/video_retrieve/$', retrieve_consumer.RetrieveVideoConsumer.as_asgi()), 
   
]
from django.urls import re_path

from .consumers import streamdata_consumer

websocket_urlpatterns = [
    re_path(r'ws/create/(?P<id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$', streamdata_consumer.StreamDataConsumer.as_asgi()),    
]
"""
ASGI config for mainapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
import blog.routing 
from blog.consumers import task_consumer
from .settings import BLOG_CREATE_CHANNEL_NAME


task_channel_name = BLOG_CREATE_CHANNEL_NAME
print("Task channel name: ", task_channel_name)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainapp.settings')

application = ProtocolTypeRouter({

    'http' : get_asgi_application(),
    'websocket': AuthMiddlewareStack(
            URLRouter(
                blog.routing.websocket_urlpatterns
            ),
        ),
    'channel': ChannelNameRouter({
            task_channel_name: task_consumer.TaskConsumer.as_asgi(),
        }),
    
})

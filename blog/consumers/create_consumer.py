from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from mainapp.settings import BLOG_CREATE_CHANNEL_NAME

# from .models import YourModel

class CreateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'Consumer connection_established',
            'message': 'Your are now connected to the server.'
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("CreateConsumer: ", text_data)
        data = json.loads(text_data)
        try:
            # Send event to start task
            await self.start_task(data)
            await self.send(text_data=json.dumps({
                'message': 'Task started successfully'
            }))
        except Exception as e:
            print("CreateConsumer error: ", e)
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))

    async def start_task(self, data):
        print("start_task: ", data)
        # Assuming you have some task to start
        await self.channel_layer.send(
            BLOG_CREATE_CHANNEL_NAME,  # Channel name where task consumer listens
            {
                'type': 'task.start',
                'data': data
            }
        )
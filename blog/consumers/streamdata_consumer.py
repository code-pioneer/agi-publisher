from channels.generic.websocket import AsyncWebsocketConsumer
import json

class StreamDataConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
       
        self.blog_id = self.scope['url_route']['kwargs']['id']
        print("blog_id: ", self.blog_id) 

        self.group_name = self.blog_id

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'Publisher connection_established',
            'message': 'Your are now connected to the server.'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': text_data
            }
        )

    async def group_message(self, event):
        value = event['message']
        print("Value: ", value)
        await self.send(text_data=json.dumps({
            'type': 'blog_message',
            'message': value
        }))
        
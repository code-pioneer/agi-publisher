from channels.generic.websocket import AsyncWebsocketConsumer
import json
from blog.agi_agent import blog_agent


class CreateBlogConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):       
        await self.accept()
        # await self.send(text_data=json.dumps({
        #     'type': 'Publisher connection_established',
        #     'message': 'Your are now connected to the server.'
        # }))

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        print("CreateConsumer: ", text_data)
        data = json.loads(text_data)
        try:
            # Send event to start task
            await blog_agent(self, 'topic', data['channel'])
            await self.disconnect(self)
        except Exception as e:
            print("CreateConsumer error: ", e)
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
        
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from blog.db import get_blog_response_by_request_id


class RetrieveBlogConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):       
        await self.accept()
        # await self.send(text_data=json.dumps({
        #     'type': 'Retrieve connection_established',
        #     'message': 'Your are now connected to the server.'
        # }))

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        print("Retreive Consumer: ", text_data)
        data = json.loads(text_data)
        try:
            response = await get_blog_response_by_request_id(data['channel'].strip())
            await self.send(text_data=json.dumps({
                'message': response
            }))
        except Exception as e:
            print("CreateConsumer error: ", e)
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
        
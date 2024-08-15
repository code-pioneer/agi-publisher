from channels.generic.websocket import AsyncWebsocketConsumer
import json
from videos.db import get_video_response_by_request_id
from datetime import datetime
import asyncio


class RetrieveVideoConsumer(AsyncWebsocketConsumer):
    
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
            latest_ts = datetime.min 
            all_blog_entries = []
        
            while True:
                blog_entries, latest_ts = await get_video_response_by_request_id(data['channel'].strip(), latest_ts)
                all_blog_entries.extend(blog_entries)
                
                if blog_entries:
                    for response in blog_entries:
                        if response.get('message'):
                            print(f"New blog entries: {response}")
                            await self.send(text_data=json.dumps({'message': response }))
                            if response.get('message') == 'DONE':
                                print(f"End of blog entries: {response}")
                                return
                await asyncio.sleep(5)  # Wait for 5 seconds before checking for new entries
           
        except Exception as e:
            print("CreateConsumer error: ", e)
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))        
            
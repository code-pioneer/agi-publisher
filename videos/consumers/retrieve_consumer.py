from channels.generic.websocket import AsyncWebsocketConsumer
import json
from videos.db import get_video_response_by_request_id, get_task_by_id, get_video_by_id
from datetime import datetime
import asyncio
from django.templatetags.static import static

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
        # print("Retreive Consumer: ", text_data)
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
                                if data['interactive']:
                                    print(f"tesing1")

                                    video_task_instance = await get_task_by_id(id=data['task_id'].strip())
                                    if video_task_instance:
                                        print(f"tesing2")

                                        while True:
                                            video_task_instance = await get_task_by_id(id=data['task_id'].strip())
                                            if video_task_instance.status == 'complete':
                                                print(f"tesing3")

                                                response = await get_video_by_id(id=data['channel'].strip())
                                                if video_task_instance.task_name == "transcript":
                                                    task_res = f'<h4 class="mb-1">{response.transcript}</h4>'
                                                elif video_task_instance.task_name == "image":
                                                    selected_theme_url = static(f'{response.imgurl}')  # Static file path
                                                    task_res = f'''<div style="position: relative;">
                                                            <img class="card-img-top" src="{selected_theme_url}">
                                                        </div>'''
                                                elif video_task_instance.task_name == "video":
                                                    selected_theme_url = static(f'{response.videourl}')  # Static file path
                                                    task_res = f'''<div style="position: relative;">
                                                            <video class="card-img-top" controls src="{selected_theme_url}" type="video/mp4">
                                                        </div>'''
                                                elif video_task_instance.task_name == "publish":
                                                     task_res = f'<h4 class="mb-1 text-center">Enjoy!</h4>' 
                                                message = {"task_response": task_res,"message": 'COMPLETE'}

                                                await self.send(text_data=json.dumps({'message': message }))
                                                return
                                            print(f"tesing4")
                                            await asyncio.sleep(5)  # Wait for 5 seconds before checking for new entries

                                return
                await asyncio.sleep(5)  # Wait for 5 seconds before checking for new entries
           
        except Exception as e:
            print("CreateConsumer error: ", e)
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))        
            
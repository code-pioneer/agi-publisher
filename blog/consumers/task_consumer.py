from channels.generic.websocket import AsyncWebsocketConsumer
import json
from blog.agi_agent import blog_agent


class TaskConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            print("TaskConsumer: connect")
            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'Task connection_established',
                'message': 'Your are now connected to the Task server.'
            }))
        except Exception as e:
            print("Error in connect:", str(e))
    
    async def disconnect(self, close_code):
        pass

    async def task_start(self, event):
        try:
            data = event['data']
            print("Task started with data:", data)
            await self.send_task_message(data)
        
        except Exception as e:
            print("Error in task_start:", str(e))
    
    async def send_task_message(self, data):
        """
        Send task message via channel layer.
        """
        print("Sending task message:", data)
        response = await blog_agent(topic=data['topic'], id=data['id'])

   
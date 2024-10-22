from langchain.agents import tool
from mainapp.settings import BASE_DIR
from videos.db import update_video_request, update_video_task

async def update_db(id, video_url, image_url, video_name, transcript, task_id):

    task_instance = await update_video_task(id=task_id)
    if task_instance.task_name != 'publish':
        await update_video_request(request_id=id, videourl=video_url, imgurl=image_url, video_name=video_name, transcript=transcript  )
    return f'DB updated'
        
@tool
async def save_to_db(id: str, video_url: str, image_url, Filename: str, transcript: str, task_id: str ) -> str:
    """Update Database."""
    print(f'save_to_db')
    return await update_db(id=id, video_url=video_url, image_url=image_url, video_name=Filename, transcript=transcript, task_id=task_id)

def setup():
    return save_to_db

def profile():
    profile = {
        "name": "publish",
        "profile": "Publisher",
        "task": "File Saving",
        "url": "assets/img/publisher.png",
    }
    return profile
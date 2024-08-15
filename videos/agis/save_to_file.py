from langchain.agents import tool
import os
import aiofiles 
from mainapp.settings import BASE_DIR
from videos.db import update_video_request

async def write_file(transcript, id, video_url, image_url, filename):

    file_path = os.path.join(BASE_DIR, 'videos', 'media', f'{filename}.txt')

    async with aiofiles.open(file_path, 'w') as file:
        await file.write(transcript)
        print(f'File saved to {file_path} {image_url}')
        await update_video_request(request_id=id, videourl=video_url, imgurl=image_url, status='published')
        return f'File saved to {file_path}'
        
@tool
async def save_to_file(transcript: str, id: str, video_url: str, image_url, Filename: str) -> str:
    """Save the final video and transcript result once video is ready."""
    print(f'save_to_file')
    return await write_file(transcript=transcript, id=id, video_url=video_url, image_url=image_url, filename=Filename)

def setup():
    return save_to_file

def profile():
    profile = {
        "name": "publish",
        "profile": "Publisher",
        "task": "File Saving",
        "url": "assets/img/publisher.png",
    }
    return profile
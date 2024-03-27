from langchain.agents import tool
import os
import aiofiles 
from mainapp.settings import BASE_DIR
from blog.db import update_blog_request

async def write_file(result, id, image_url, filename, topic):
    if 'html' in result:
        file_path = os.path.join(BASE_DIR, 'blog', 'media', f'{filename}.html') 
    else:
        file_path = os.path.join(BASE_DIR, 'blog', 'media', f'{filename}.md')

    async with aiofiles.open(file_path, 'w') as file:
        await file.write(result)
        print(f'File saved to {file_path} {image_url}')
        await update_blog_request(request_id=id, blogurl=file_path, imgurl=image_url, status='published', topic=topic)
        return f'File saved to {file_path}'
        
@tool
async def save_to_file(result: str, id: str, image_url: str, Filename: str, topic: str) -> str:
    """Save the final blog post result using the generated file."""
    print(f'save_to_file')
    return await write_file(result=result, id=id, image_url=image_url, filename=Filename, topic=topic)

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
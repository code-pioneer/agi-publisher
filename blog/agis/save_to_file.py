from langchain.agents import tool
import os
import aiofiles 
from mainapp.settings import BASE_DIR
from blog.db import update_blog_request

async def write_file(result, id, image_url, filename):
    file_path = os.path.join(BASE_DIR, 'blog', 'media', filename) 
    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # file_name = f'blog_{timestamp}'
    # filename = os.path.basename(f"/blog/content/{filename}")

    # file_path = os.path.join(BASE_DIR, 'content', filename)
    async with aiofiles.open(file_path, 'w') as file:
        await file.write(result)
        print(f'File saved to {file_path} {image_url}')
        index = image_url.find('/assets')
        if index != -1:
            image_url = image_url[index:]
        await update_blog_request(request_id=id, blogurl=file_path, imgurl=image_url, status='published')
        await update_blog_request(request_id=id, blogurl=file_path, imgurl=image_url, status='published')
        return f'File saved to {file_path}'
        
@tool
async def save_to_file(result: str, id: str, image_url: str, filename: str) -> str:
    """Save the final blog post result using the correct file type."""
    print(f'save_to_file')
    return await write_file(result=result, id=id, image_url=image_url, filename=filename)

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
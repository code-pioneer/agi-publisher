from langchain.agents import tool
import os
import aiofiles 
from mainapp.settings import BASE_DIR

async def write_file(result, filename):
    file_path = os.path.join(BASE_DIR, 'blog', 'media', filename) 
    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # file_name = f'blog_{timestamp}'
    # filename = os.path.basename(f"/blog/content/{filename}")

    # file_path = os.path.join(BASE_DIR, 'content', filename)
    async with aiofiles.open(file_path, 'w') as file:
        await file.write(result)
        
@tool
async def save_to_file(result: str, filename: str) -> str:
    """Save the final blog post result using the correct file type."""
    print(f'save_to_file')
    return await write_file(result=result,filename=filename)

def setup():
    return save_to_file

def profile():
    return '📢 Publish'
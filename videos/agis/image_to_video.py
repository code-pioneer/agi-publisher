import os
import aiofiles
from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import Callbacks
import requests
from mainapp.settings import IMAGE_GEN_MODEL,SIZE, BASE_DIR
from openai import OpenAI
import cv2



async def create_video(image_url, filename):

    output_video = f"{filename}.mp4"
    image_name = f"{filename}.png"
    image_url = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', image_name) 
    video_url = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', output_video) 

    print('image_url', image_url)

    # Load the image
    image = cv2.imread(image_url)

    # Get the image dimensions

    height, width, _ = image.shape

    # Define the video properties
    fps = 30  # Frames per second
    duration = 5  # Duration in seconds
    total_frames = fps * duration

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_url, fourcc, fps, (width, height))

    # Write the image as multiple frames to create a video
    for _ in range(total_frames):
        video.write(image)

    # Release the video writer
    video.release()
    cv2.destroyAllWindows()

    
@tool
async def image_to_video(image_url: str, Filename: str, callbacks: Callbacks) -> str:
    """Convert image to a video once image is generated."""
    print("inside image_to_video")
    return await create_video(image_url=image_url, filename=Filename)
    


def setup():
    return image_to_video

def profile():
    profile = {
        "name": "Image to Video",
        "profile": "Art Illustrator",
        "task": "Video Generation",
        "url": "assets/img/artist.png",
    }
    return profile


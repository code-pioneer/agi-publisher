import os
import aiofiles
from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import Callbacks
import requests
from mainapp.settings import IMAGE_GEN_MODEL,SIZE, BASE_DIR, LONG_VIDEO_SIZE, SHORT_VIDEO_SIZE
from openai import OpenAI
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS
from pydub import AudioSegment
import json




def generate_voice_over(transcript, duration, filename):
    # Convert text to speech using gTTS
    tts = gTTS(transcript, lang='en')
    audio_name = f'{filename}.mp3'
    audio_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', 'audio',audio_name) 

    tts.save(audio_path)


    # Load the generated audio
    audio = AudioSegment.from_mp3(audio_path)

    # Adjust the length of the audio to match the video duration
    audio_duration = len(audio) / 1000.0  # Duration in seconds
    if audio_duration > duration:
        # Trim the audio if it's longer than the video duration
        audio = audio[:duration * 1000]
    elif audio_duration < duration:
        # Loop the audio to match the video duration
        repeats = int(duration / audio_duration) + 1
        audio = (audio * repeats)[:duration * 1000]

    # Export the adjusted audio
    audio.export(audio_path, format='mp3')

    return audio_path

async def create_video(transcript, size, filename):

    processed_video_name = f"{filename}.mp4"
    image_name = f"{filename}.png"
    image_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', image_name) 
    video_duration = size

    audio_path = generate_voice_over(transcript, video_duration, filename)

    # Create an ImageClip
    image_clip = ImageClip(image_path, duration=video_duration)
    scroll_speed = 25.0
    # Create the scrolling text
    txt_clip = TextClip(transcript, font='Roboto', fontsize=55, color='white', size=(image_clip.w, None), method='caption')
    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(video_duration)

    # Scroll the text
    txt_clip = txt_clip.set_start(0).set_duration(video_duration).set_position(lambda t: ('center', -t * scroll_speed))
    
    # Add the voice-over audio to the video
    audio_clip = AudioFileClip(audio_path).set_duration(video_duration)

    # Composite the text over the image and audio
    video = CompositeVideoClip([image_clip, txt_clip])
    video = video.set_audio(audio_clip)

    # Save the processed video
    processed_video_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', 'video', processed_video_name) 

    video.write_videofile(processed_video_path, codec='libx264', fps=24)

    index = processed_video_path.find('/assets')
    if index != -1:
        processed_video_path = processed_video_path[index:]

    return {'video_url':processed_video_path}

    
@tool
async def generate_video(transcript: str, blog_params: str, image_url: str, Filename: str, callbacks: Callbacks) -> str:
    """Convert image to a video using generated image and transcript."""
    print("inside generate_video")
    blog_params_json = json.loads(blog_params)
    in_depth = blog_params_json.get("in_depth", False)
    if in_depth:
        size = LONG_VIDEO_SIZE
    else:
        size = SHORT_VIDEO_SIZE
    return await create_video(transcript=transcript, size=size,filename=Filename)
    


def setup():
    return generate_video

def profile():
    profile = {
        "name": "Generate Video",
        "profile": "Video Illustrator",
        "task": "Video Generation",
        "url": "assets/img/artist.png",
    }
    return profile


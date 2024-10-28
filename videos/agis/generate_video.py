import os
import aiofiles
from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import Callbacks
import requests
from mainapp.settings import IMAGE_GEN_MODEL,SIZE, BASE_DIR, LONG_VIDEO_SIZE, SHORT_VIDEO_SIZE
from openai import OpenAI
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip
from gtts import gTTS
from pydub import AudioSegment
import json
import random




def audio_to_text(audio_path):
    print('audio_to_text')
    audio_file = open(audio_path, "rb")
    client = OpenAI()
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )

    # List to hold the TextClips for each word
    text_clips = []

    # Create TextClips for each word and sync with word timings
    for word_info in transcript.words:
        word = word_info['word']
        start_time = word_info['start']
        end_time = word_info['end']
        
        # Create a TextClip for the word
        if word:
            txt_clip = TextClip(word, fontsize=55, color='white', font='Roboto')
            
            # Set the position and duration of the TextClip
            txt_clip = (txt_clip.set_position(("center", "center"))  # Position of the word on the screen
                                .set_start(start_time)               # Start time from the transcript
                                .set_duration(end_time - start_time)) # Duration the word appears
            
            # Append the TextClip to the list
            text_clips.append(txt_clip)
    return text_clips

def add_textclips_bg(text_clips, image_clip, duration):
    padding = 20
    # Get the width of the image for background width
    image_width, image_height = image_clip.size

    # Create a single background ColorClip for the entire duration
    bg_height = 100  # Set a fixed height for the background
    bg_color = ColorClip(size=((image_width - 2*padding), bg_height), color=(0, 0, 0))  # Black background
    bg_color = bg_color.set_opacity(0.6)  # Semi-transparent background

    # Set the background to last for the entire duration of the video
    bg_color = bg_color.set_position(('center', image_height - bg_height - padding)).set_duration(duration)    
    text_clips_with_bg = [bg_color]  # Start with the background

    for txt_clip in text_clips:
        # Set the text position inside the background (accounting for the padding)
        text_vertical_position = (image_height - bg_height - padding + (bg_height - txt_clip.size[1]) / 2)
    
        txt_clip = txt_clip.set_position(('center', text_vertical_position)).set_duration(txt_clip.duration)

        # Add the text clip to the list (background is already added for full duration)
        text_clips_with_bg.append(txt_clip)
    return text_clips_with_bg

def generate_voice_over(transcript, filename, voice):
    print('generate_voice_over')
    audio_name = f'{filename}.mp3'
    audio_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', 'audio',audio_name) 
    if voice is not None:
        select_voice = voice
    else:
        voice_choice = ("alloy", "echo", "fable", "onyx", "nova", "shimmer") 
        select_voice=random.choice(voice_choice)

    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=select_voice,
        input=transcript
    )
    response.stream_to_file(audio_path)

    return audio_path

async def create_video(transcript, filename, voice):

    processed_video_name = f"{filename}.mp4"
    image_name = f"{filename}.png"
    image_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', image_name) 

    audio_path = generate_voice_over(transcript, filename, voice)
    text_clips = audio_to_text(audio_path)
    audio_clip = AudioFileClip(audio_path)

    duration = audio_clip.duration

    # Create an ImageClip
    image_clip = ImageClip(image_path, duration=duration)

    text_clips_with_bg = add_textclips_bg(text_clips, image_clip, duration)

    # Create VideoClip
    video = CompositeVideoClip([image_clip] + text_clips_with_bg)
    video = video.set_audio(audio_clip)

    # Save the processed video
    processed_video_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', 'video', processed_video_name) 

    video.write_videofile(processed_video_path, codec='libx264', audio_codec='aac', fps=24)

    index = processed_video_path.find('/assets')
    if index != -1:
        processed_video_path = processed_video_path[index:]

    return {'video_url':processed_video_path}

    
@tool
async def generate_video(transcript: str, video_params: str, image_url: str, Filename: str, callbacks: Callbacks) -> str:
    """Convert image to a video using generated image and transcript."""
    print("inside generate_video")
    print(f'VIDEO_PARAMS: {video_params}')
    video_params_json = json.loads(video_params)
    voice = video_params_json.get("voice", False)
    return await create_video(transcript=transcript, filename=Filename, voice=voice)
    


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


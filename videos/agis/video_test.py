from openai import OpenAI
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip
from pathlib import Path
# from generate_video import create_video
import os
import random
BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)
def audio_to_text(audio_path):
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
        txt_clip = TextClip(word, fontsize=55, color='white', font='Roboto')
        
        # Set the position and duration of the TextClip
        txt_clip = (txt_clip.set_position(("center", "center"))  # Position of the word on the screen
                            .set_start(start_time)               # Start time from the transcript
                            .set_duration(end_time - start_time)) # Duration the word appears
        
        # Append the TextClip to the list
        text_clips.append(txt_clip)
    return text_clips

def add_textclips_bg(text_clips, image_clip, duration):
    padding = 50
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

def generate_voice_over(transcript, filename):
    audio_name = f'{filename}.mp3'
    audio_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', 'audio',audio_name) 
    voice_choice = ("alloy", "echo", "fable", "onyx", "nova", "shimmer") 
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=random.choice(voice_choice),
        input=transcript
    )
    response.stream_to_file(audio_path)

    return audio_path

def create_video(transcript, filename):

    processed_video_name = f"{filename}.mp4"
    image_name = f"{filename}.png"
    image_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', image_name) 

    audio_path = generate_voice_over(transcript, filename)
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

if __name__ == "__main__":
    create_video("Today is a wonderful day to build something people love!","aaa_bank_financial_report_135020")
    # audio_to_text()

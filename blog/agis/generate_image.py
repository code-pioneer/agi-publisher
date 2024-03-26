import os
import aiofiles
from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import Callbacks
import requests
from mainapp.settings import IMAGE_GEN_MODEL,SIZE, BASE_DIR
from openai import OpenAI

@tool
async def generateImage(topic: str, Filename:str, callbacks: Callbacks) -> str:
    """Generate an approriate Image once filename is generated."""
    print("inside generateImage")
    #llm = OpenAI(temperature=0.9,streaming=STREAMING,model=IMAGE_GEN_MODEL)
    llm = OpenAI()
    
    image_template = PromptTemplate.from_template(
    """You are an AI Image Generation model. Your objective is to generate a digital vibrant image for given Blog content:
    Send Image url in the answer
    Blog: {topic}
    
    Answer: """
    )
    
    task = image_template.format(topic=topic)
    print('task', task)
    result = llm.images.generate(model=IMAGE_GEN_MODEL,
        prompt=task,
            size=SIZE,
            quality="standard",
            n=1,)
    
    print(f'result={result}')
    print(f"image url={result.data[0].url}")
    # Save the generated image
    if result:
        image_url=result.data[0].url
        return await saveImage(image_url,Filename)

def setup():
    return generateImage

def profile():
    profile = {
        "name": "generateImage",
        "profile": "Art Illustrator",
        "task": "Image Generation",
        "url": "assets/img/artist.png",
    }
    return profile

async def saveImage(image_url,fileName):
    
    # imageFileName= fileName.replace(".html","_title.png")
    filename = f"{fileName}.png"
    file_path = os.path.join(BASE_DIR, 'home', 'static', 'assets','media', filename) 

    print(file_path)
    # Download the image data
    image_data = requests.get(image_url).content
    # Save the image
    async with aiofiles.open(file_path, 'wb') as file:
        # str_data = image_data.decode('utf-8')
        await file.write(image_data)
    index = file_path.find('/assets')
    if index != -1:
        file_path = file_path[index:]

    print(f"Image saved {file_path}")
    return {'image_url': file_path}

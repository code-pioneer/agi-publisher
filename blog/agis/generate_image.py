import os
import aiofiles
from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import Callbacks
import requests
from mainapp.settings import IMAGE_GEN_MODEL,SIZE
from openai import OpenAI

@tool
async def generateImage(answer: str, fileName:str, callbacks: Callbacks) -> str:
    """After proofreading of blog is completed, generate an approriate image using generated Blog Content."""
    print("inside generateImage")
    #llm = OpenAI(temperature=0.9,streaming=STREAMING,model=IMAGE_GEN_MODEL)
    llm = OpenAI()
    
    image_template = PromptTemplate.from_template(
    """You are an AI Image Generation model. Your objective is to generate a digital vibrant image for given Blog content:
    Send Image url in the answer
    Blog: {answer}
 
    Answer: """
    )
    
    task = image_template.format(answer=answer)
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
        return await saveImage(image_url,fileName)

def setup():
    return generateImage

def profile():
    return '🎨 Art Illustrator'

async def saveImage(image_url,fileName):
    
    imageFileName= fileName.replace(".html","_title.png")
    filename = os.path.basename(f"/blog/content/{imageFileName}.png")
    print(filename)
    # Download the image data
    image_data = requests.get(image_url).content
    # Save the image
    async with aiofiles.open(filename, 'w') as file:
        await file.write(image_data)

    print(f"Image saved {filename}")
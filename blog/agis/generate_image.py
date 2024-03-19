from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import Callbacks
from mainapp.settings import IMAGE_GEN_MODEL, STREAMING,SIZE
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from openai import OpenAI

@tool
async def generateImage(answer: str, callbacks: Callbacks) -> str:
    """When the blog is ready to be published, generate an approriate image using generated Blog Content."""
    print("inside generateImage")
    #llm = OpenAI(temperature=0.9,streaming=STREAMING,model=IMAGE_GEN_MODEL)
    llm = OpenAI()
    
    image_template = PromptTemplate.from_template(
    """You are an AI Image Generation model. Your objective is to generate an image for given Blog:
    Blog: {answer}
 
    Answer: """
    )
    
    task = image_template.format(answer=answer)
    print('task', task)
    result = llm.images.generate(model=IMAGE_GEN_MODEL,
        prompt=task,
            size="1024x1024",
            quality="standard",
            n=1,)
    return result

def setup():
    return generateImage

def profile():
    return '🎨 Art Illustrator'
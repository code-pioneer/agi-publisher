from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from mainapp.settings import LLM_MODEL
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING

@tool
async def generate_filename(topic: str, callbacks: Callbacks) -> str:
    """Generate filename for a given topic"""
    print(f'generate_filename')
    save_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to generate proper file name for a given Topic:
    Come up with file name with in 50 letters.
    Append timestamp of Hours, Minutes, Seconds in the format: <filename>_"%H%M%S" to avoid overwriting.
    
    Topic: {topic}

    Answer: 
    Reasoning: Reasoning behind the filename and file extension.
    Filename: """
    )
    
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0, streaming=STREAMING)
    chain = save_blog_template | llm.with_config(
        {
            "run_name": "Generate Filename",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"topic": topic})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return generate_filename

def profile():
    profile = {
        "name": "publish",
        "profile": "Publisher",
        "task": "Video Naming",
        "url": "assets/img/publisher.png",
    }
    return profile

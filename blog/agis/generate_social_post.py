from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING

@tool
async def generate_post_content(blog: str, image_url: str, callbacks: Callbacks) -> str:
    """Generate social post content after save_to_file task is executed."""
    print(f'generatePostContent')

    post_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to create an Eloquent tweet from the blog content.:
    Do not ommit any content. 
    Important: Remove "Thoughts", "Infuence", "Ignored" from the blog content.
    Important: Include Image url in bottom of tweet content and align to center.
   
    Blog: {blog}
    Image: {image_url}

    Answer format should be. 
     
    Answer: """
)
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.9, streaming=STREAMING)
    chain = post_template | llm.with_config(
        {
            "run_name": "Generate Post Content",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"blog": blog, "image_url" : image_url})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return generate_post_content
  
def profile():
    profile = {
        "name": "social",
        "profile": "Social",
        "task": "Social Post Content",
        "url": "assets/img/social-avatar.png",
    }
    return profile

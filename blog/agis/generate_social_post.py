from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING

@tool
async def generate_social_post(blog: str, image_url: str, callbacks: Callbacks) -> str:
    """Generate social post content."""
    print(f'generatePostContent')

    post_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to create SEO friendly 5 tweets from the blog content.:
    Do not ommit any content. 
    Important: Remove "Thoughts", "Infuence", "Ignored" from the blog content.
    Important: Feel free to include emojis and icons.
    Important: Consider tweets are for "Millennials", "Gen Z", and "Gen Alpha"
    Important: DO Not number like 1, 2, 3 to the generated tweets
    Important: refain from indexing the tweets.
    Blog: {blog}
    Image: {image_url}

    Answer format should be. 
     
    Answer: """
)
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.9, streaming=STREAMING)
    chain = post_template | llm.with_config(
        {
            "run_name": "Generate Social Post",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"blog": blog, "image_url" : image_url})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return generate_social_post
  
def profile():
    profile = {
        "name": "social",
        "profile": "Social",
        "task": "Social Post Content",
        "url": "assets/img/social-avatar.png",
    }
    return profile

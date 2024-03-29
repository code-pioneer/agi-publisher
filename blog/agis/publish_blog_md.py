from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING

@tool
async def publish_blog_md(blog: str, image_url: str,callbacks: Callbacks) -> str:
    """When the blog is ready to be published, convert it to Markdown format."""
    print(f'publish_blog_md')

    md_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to convert given Blog in to Mark down text for Blog publication:

    Important: Remove "Thoughts", "Infuence", "Ignored" from the blog content.
    
    Important: Include Image url in top of blog content.
    Important: Make sure image size properly fits the blog content.
    Important: Use the following format for image tag: ![image]({image_url})
    Important: Use Heading tags for Title and Subtitles.
    Important: Use Paragraph tags for content.
    Important: Use List tags for list items.
    Important: Use Blockquote tags for quotes.
    Important: Use Anchor tags for links.
    Important: Use Image tags for images.
    Important: Use Strong and Em tags for emphasis.
    Important: Use Table tags for tables.
    



    Blog: {blog}
    Image: {image_url}


    Answer format should be. 
 
    Answer: """
    )
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0, streaming=STREAMING)
    chain = md_blog_template | llm.with_config(
        {
            "run_name": "Publish Blog Md",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"blog": blog, "image_url" : image_url})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return publish_blog_md

def profile():
    profile = {
        "name": "publish",
        "profile": "Publisher",
        "task": "Markdown Preping",
        "url": "assets/img/publisher.png",
    }
    return profile
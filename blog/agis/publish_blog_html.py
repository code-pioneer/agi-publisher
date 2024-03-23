from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING

@tool
async def publishBlogHtml(blog: str, image_url: str, callbacks: Callbacks) -> str:
    """When the blog is ready to be published, convert it to HTML format."""
    print(f'publishBlogHtml')

    html_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to convert given Blog in to HTML text for Blog publication:
    Do not ommit any content. 
    Avoid using href. 
    Important: Remove "Thoughts", "Infuence", "Ignored" from the blog content.
    Important: Include Image url in top of blog content and align to center.
    important: Use the following format for image tag: <img src="{image_url}" alt="image">
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
    chain = html_blog_template | llm.with_config(
        {
            "run_name": "Publish Blog Html",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"blog": blog, "image_url" : image_url})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return publishBlogHtml
  
def profile():
    profile = {
        "name": "publish",
        "profile": "Publisher",
        "task": "HTML Preping",
        "url": "assets/img/publisher.png",
    }
    return profile

from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING

@tool
async def publish_blog_html(blog: str, image_url: str, callbacks: Callbacks) -> str:
    """When the blog is ready to be published with generated image, convert it to HTML format."""
    print(f'publish_blog_html')

    html_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to convert given Blog in to pretty HTML5 text for Blog publication:

    Important: Include Image url in top of blog content and align to center.
    important: Use the following format for image tag: <img src="/static{image_url}" alt="image" style="display: block;margin: 0 auto;margin-bottom: 20px;">

    Include Bootstrap's CSS from BootstrapCDN
    Add Bootstrap container
    Include Bootstrap's JavaScript from BootstrapCDN

    Add padding to the container.
    Add paragraph tags for content.

    Important: Remove "Thoughts", "Infuence", "Ignored" content from the blog content.
    Important: DO NOT Remove "SEO Tags" content from the blog content. Add # to each SEO Tags to increase visibility.
    Important: Add paragraph heading 'SEO TAGS' to the SEO Tags section.


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
    return publish_blog_html
  
def profile():
    profile = {
        "name": "publish",
        "profile": "Publisher",
        "task": "HTML Preping",
        "url": "assets/img/publisher.png",
    }
    return profile

from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING
from blog.db import get_blog_by_id
from datetime import datetime

@tool
async def publish_blog_html(blog: str, image_url: str, id: str, callbacks: Callbacks) -> str:
    """When the blog is ready to be published with generated image, convert it to HTML format."""
    print(f'publish_blog_html')

    html_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to convert given Blog in to pretty HTML5 text for Blog publication:
    Include following head tag.
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
            <link rel="shortcut icon" type="image/png" href="/static/assets/img/favicon.png"/>
            <link rel="stylesheet" href="/static/assets/fonts/feather/feather.css" />
            <link rel="stylesheet" href="/static/assets/css/taralnest.min.css">
        </head>
    use below div to include for main content.

        <div class="container text-bg-light" id="main-content" style="padding: 50px">  

    Blog Title must be at top of the page and align to center.

    Below Title, add below div to include card for user profile.
        <div class="row" style="text-align: center;>
            <div class="col">
                <img src="/static/assets/img/social-avatar.png" class="avatar-img rounded-circle avatar-sm"
                    alt="Avatar Image"> <b> {user} </b>
                    <span class="tiny text-body-secondary"><i class="bi bi-clock"></i> {blog_ts}</span>
            </div>
        </div>
                

    Include Image url after title & user profile and align to center.
    Add image tag: <img src="{image_url}" alt="image" style="display: block;margin: 0 auto;margin-top: 20px;margin-bottom: 20px;width: 50%""

    Add paragraph tags for content.

    Important: Remove "Thoughts", "Infuence", "Ignored" content from the blog content.
    Important: DO NOT Remove "SEO Tags" content from the blog content. 
    Important: Add h4 heading 'SEO TAGS' to the SEO Tags section if exists.
    <h4>SEO TAGS</h4>
    Important: Use below format to list each SEO Tags to increase visibility and enclose each SEO Tags in badges.


        <p>
            <span class="badge text-bg-secondary">#seo tags</span>
        </p>

    Add following script tags before closing body tag.
        <script src="/static/assets/js/jquery-3.7.1.min.js"></script>
        <script src="/static/assets/js/bootstrap.bundle.min.js"></script>
        <script src="/static/assets/js/highlight.min.js"></script>


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
    image_url = f'/static{image_url}'
    blog_instance = await get_blog_by_id(id.strip())
    user = blog_instance.user
    blog_ts = blog_instance.ts
    formatted_timestamp = datetime.strptime(blog_ts, "%Y-%m-%d %H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M")

    chunks = [chunk async for chunk in chain.astream({"blog": blog, "image_url" : image_url, 'user': user, 'blog_ts': formatted_timestamp})]
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

from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING
import json


@tool
async def create_blog(content: str, topic: str, blog_params: str, callbacks: Callbacks) -> str:
    """Generate a blog from the output of search results."""
    print(f'createBlog')
    create_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to write a {theme} blog post on the topic {topic}. 
    Use the relevant context provided to create a {theme} blog post. Do not limit yourself to the context; feel free to add your insights and examples to enrich the content.
    Blog size must be based on this guidelines - {size}.
    Use the provided guidelines. 
    
    Guidelines: Add an appropriate Blog title as the Blog heading.
    Start with a compelling hook to grab the reader's attention and briefly introduce the topic's significance. Provide a succinct overview of what the blog post will cover, including the main thesis or argument.
    
    Divide the body into three paragraphs, each focusing on a specific aspect or subtopic related to the main theme. Use topic sentences to introduce main ideas and support them with evidence or examples. Ensure smooth transitions between paragraphs to maintain coherence.

    Summarize the main points discussed in the body paragraphs and restate the thesis or main argument. End with a thought-provoking statement or call to action to leave a lasting impression on the reader.

    Compile a concise list of sources used in the blog post, providing proper attribution and bibliographic details at the end of the post. 
    
    Refrain from using titles such as Introduction, Conclusion, body, paragraph numbers.
    Blog Size Guidelines: {size}
    Topic: {topic}
    Context: {content}
    Theme: {theme}
    Search_engine_optimization: {seoText}
    Response must be in the following format.

    Answer: 
        Blog:  
        SEO Tags:
        Thoughts: Include 5 keywords that highlight your thoughts and reasoning while coming up with this blog content.
        Influence: 5 points that influenced your thoughts.
        Ignored: 5 points that you discarded."""

    )
    print(f'BLOG_PARAMS: {blog_params}')
    blog_params_json = json.loads(blog_params)
    seo = blog_params_json.get("seo", False)
    in_depth = blog_params_json.get("in_depth", False)
    theme = blog_params_json.get("theme", "descriptive")
    if in_depth:
        size = f'Make sure that Blog is in-depth. Provide detailed information and insights. The blog should be a minimum of 2000 words and a maximum of 3000 words.'
    else:
        size = f'Make sure that it is a Micro Blog with a minimum of 500 words and a maximum of 1000 words.'
    if seo:
        seoText = f'Make sure to generate SEO tags for the blog to improve search engine visibility.'
    else:
        seoText = f'No need to generate SEO tags.'
    if theme == 'humor':
        theme = f'humor-style '
    elif theme == 'persuasive-style':
        theme = f'persuasive '
    elif theme == 'informative':
        theme = f'informative-style '
    elif theme == 'narrative':
        theme = f'narrative-style '
    elif theme == 'descriptive':
        theme = f'descriptive-style '
    elif theme == 'expository':
        theme = f'expository-style '

    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.9, streaming=STREAMING)
    chain = create_blog_template | llm.with_config(
        {
            "run_name": "Create Blog LLM",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"content": content, "topic" : topic, 'size': size, 'seoText': seoText, 'theme': theme})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return create_blog

def profile():
    profile = {
        "name": "create",
        "profile": "Creator",
        "task": "Blog Writing",
        "url": "assets/img/creater.png",
    }
    return profile

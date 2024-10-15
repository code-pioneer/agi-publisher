from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING, SHORT_VIDEO_SIZE, LONG_VIDEO_SIZE
import json
from . themes import themes



@tool
async def generate_transcript(content: str, topic: str, blog_params: str, callbacks: Callbacks) -> str:
    """Generate transcript for video production"""
    print(f'generate_transcript')
    create_blog_template = PromptTemplate.from_template(
    """
    Imagine you're creating a script for a {size} video on {topic}. Keep the script with in {words} words.
    Please strictly follow the below provided theme while creating the script.
    Theme: {theme}
    
    Response must be in the following format as show in the example.

    Example:

Hey there, ever wondered what makes the Empire State Building in New York City so iconic? Let's dive in!

First off, did you know that the Empire State Building stands at a staggering 1,454 feet tall, making it one of the tallest buildings in the world? It's a total skyscraper superstar!

Not only is it tall, but this masterpiece was built in just 410 days during the Great Depression - talk about a speedy construction project!

And get this, the Empire State Building has been featured in countless movies, TV shows, and even songs. It's a true symbol of New York City!

So, next time you're in the Big Apple, make sure to check out the Empire State Building and take in the breathtaking views from the top!

Thanks for watching, and don't forget to hit that like button and subscribe for more fun facts about iconic landmarks!

SEO Tags:
Empire State Building, New York City, iconic landmarks, skyscraper, Great Depression, movies, TV shows, tourism, travel, breathtaking views, Big Apple.

    """

    )
    print(f'BLOG_PARAMS: {blog_params}')
    blog_params_json = json.loads(blog_params)
    in_depth = blog_params_json.get("in_depth", False)
    if in_depth:
        size = f'long {LONG_VIDEO_SIZE} seconds with text scrolling speed of 25.0 pixels per second'
        words = 650
    else:
        size = f'short {SHORT_VIDEO_SIZE} seconds with text scrolling speed of 25.0 pixels per second.'
        words = 130
    seoText = f'Make sure to generate SEO tags for the video to improve search engine visibility.'

    theme_id = blog_params_json.get("theme", False)
    if theme_id:
        selected_theme = next((theme for theme in themes if theme['theme_id'] == theme_id), None)
        theme_prompt = selected_theme["prompt"]
    else:
        selected_theme = next((theme for theme in themes if theme['theme_id'] == "build"), None)
        theme_prompt = selected_theme["prompt"]





    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.9, streaming=STREAMING)
    chain = create_blog_template | llm.with_config(
        {
            "run_name": "Create Blog LLM",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"content": content, "topic" : topic, 'size': size, "theme": theme_prompt, "words": words,'seoText': seoText})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return generate_transcript

def profile():
    profile = {
        "name": "create",
        "profile": "Creator",
        "task": "Transcript Creation",
        "url": "assets/img/creater.png",
    }
    return profile

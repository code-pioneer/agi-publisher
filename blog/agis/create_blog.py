from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING


@tool
async def createBlog(answer: str, topic: str, callbacks: Callbacks) -> str:
    """Generate a blog from the output of search results."""
    print(f'createBlog')
    create_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to write a structured blog post using context for a given topic.
    Use the provided guidelines. Blog must have a title.
    
    Guidelines: Start with a compelling hook to grab the reader's attention and briefly introduce the topic's significance. Provide a succinct overview of what the blog post will cover, including the main thesis or argument. Keep it to 100 words.
    
    Divide the body into three paragraphs, each focusing on a specific aspect or subtopic related to the main theme. Use topic sentences to introduce main ideas and support them with evidence or examples. Ensure smooth transitions between paragraphs to maintain coherence. Keep it to 300 words.

    Summarize the main points discussed in the body paragraphs and restate the thesis or main argument. End with a thought-provoking statement or call to action to leave a lasting impression on the reader. Keep it to approximately 100 words.

    Compile a concise list of sources used in the blog post, providing proper attribution and bibliographic details at the end of the post. 
    
    Topic: {topic}
    Context: {answer}
    Response must be in the following format.

    Answer: 
        Blog:
        Thoughts: Include 5 keywords that highlights your thoughts and reasoning while coming up with this blog content.
        Infuence: 5 points that infuenced your thoughts.
        Ignored: 5 points that you discarded."""

    )
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.9, streaming=STREAMING)
    chain = create_blog_template | llm.with_config(
        {
            "run_name": "Create Blog LLM",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"answer": answer, "topic" : topic})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return createBlog

def profile():
    profile = {
        "name": "create",
        "profile": "Creator",
        "task": "Blog Writing",
        "url": "assets/img/creater.png",
    }
    return profile

from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, TOOLS, STREAMING

@tool
async def publishBlogHtml(blog: str, callbacks: Callbacks) -> str:
    """When the blog is ready to be published, convert it to HTML format."""
    print(f'publishBlogHtml')

    html_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to convert given Blog in to HTML text for Blog publication:
    Do not ommit any content. 
    Avoid using href. 

    Blog: {blog}

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
    chunks = [chunk async for chunk in chain.astream({"blog": blog})]
    return "".join(chunk.content for chunk in chunks)

TOOLS.append(publishBlogHtml)
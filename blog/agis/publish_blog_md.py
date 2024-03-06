from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, TOOLS, STREAMING

@tool
async def publishBlogMD(blog: str, callbacks: Callbacks) -> str:
    """When the blog is ready to be published, convert it to Markdown format."""
    print(f'publishBlogMD - {blog}')

    md_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to convert given Blog in to Mark down text for Blog publication:
    Do not ommit any content.  
    Do not include save_to_file in html href.

    Blog: {blog}

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
    chunks = [chunk async for chunk in chain.astream({"blog": blog})]
    return "".join(chunk.content for chunk in chunks)

TOOLS.append(publishBlogMD)
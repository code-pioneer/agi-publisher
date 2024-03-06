from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, TOOLS, STREAMING

@tool
async def reviseBlog(blog: str, feedback: str, callbacks: Callbacks) -> str:
    """Revise the blog when proofreading is complete and revisions are needed."""
    print(f'reviseBlog - {feedback}')
    revise_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to review profreading feedback and revise the given blog post.
        
    Blog: {blog}
    Feedback: {feedback}
     
    Answer: """
    )
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0, streaming=STREAMING)
    chain = revise_blog_template | llm.with_config(
        {
            "run_name": "Publish Blog Html",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"blog": blog,"feedback": feedback})]
    return "".join(chunk.content for chunk in chunks)

TOOLS.append(reviseBlog)
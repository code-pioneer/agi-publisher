from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from mainapp.settings import LLM_MODEL


@tool
def reviseBlog(blog: str, feedback: str) -> str:
    """Revise the blog when proofreading is complete and revisions are needed."""
    print(f'reviseBlog - {feedback}')
    revise_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to review profreading feedback and revise the given blog post.
        
    Blog: {blog}
    Feedback: {feedback}
     
    Answer: """
    )
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    task = revise_blog_template.format(blog=blog, feedback=feedback)
    return llm.invoke(task)

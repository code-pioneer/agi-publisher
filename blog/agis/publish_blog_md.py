from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from mainapp.settings import LLM_MODEL

@tool
def publishBlogMD(blog: str) -> str:
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
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    task = md_blog_template.format(blog=blog)
    return llm.invoke(task)
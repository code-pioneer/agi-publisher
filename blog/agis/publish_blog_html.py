from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from mainapp.settings import LLM_MODEL

@tool
def publishBlogHtml(blog: str) -> str:
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
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    task = html_blog_template.format(blog=blog)
    return llm.invoke(task)
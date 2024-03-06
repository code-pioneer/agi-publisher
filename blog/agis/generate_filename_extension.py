from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from mainapp.settings import LLM_MODEL


@tool
def generate_filename(result: str) -> str:
    """Generate filename once blog is ready to be saved."""
    print(f'generate_filename')
    save_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to generate proper file name for a given Blog:
    Come up with shorter file name.
    Append ramdom number between 1 and  1000 to filename in the format: <filename>_xxxx to avoid overwriting.
    Check the Blog content to determine the file type.
    When Blog content is of html text, then use html file extension.
    When Blog content is of Mark Down text, then use MD file extension.

    Do not ommit any content.  

    Blog: {blog}


    Answer: 
    Filename: """
    )
    
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    task = save_blog_template.format(blog=result)
    return llm.invoke(task)
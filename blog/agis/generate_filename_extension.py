from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from mainapp.settings import LLM_MODEL
from langchain_core.callbacks import Callbacks
from mainapp.settings import LLM_MODEL, STREAMING

@tool
async def generate_filename(result: str, callbacks: Callbacks) -> str:
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
    
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0, streaming=STREAMING)
    chain = save_blog_template | llm.with_config(
        {
            "run_name": "Generate Filename",
            "tags": ["tool_llm"],
            "callbacks": callbacks, 
        }
    )
    chunks = [chunk async for chunk in chain.astream({"blog": result})]
    return "".join(chunk.content for chunk in chunks)

def setup():
    return generate_filename
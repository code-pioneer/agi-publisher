from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from mainapp.settings import LLM_MODEL


@tool
def proofreadingBlog(blog: str) -> str:
    """Proofread the blog once it's generated."""
    print(f'proofreadingBlog')

    proofreading_blog_template = PromptTemplate.from_template(
    """You are an AI language model Blog Proofreading assistant. 
    
    Your objective is to meticulously review given Blog content to correct errors in grammar, punctuation, spelling, and syntax. 
    It ensures clarity, coherence, and consistency in the text, enhancing its overall readability and professionalism. 
    Proofreading also involves checking for formatting issues and ensuring adherence to style guidelines or specific requirements. 
    Ultimately, the goal is to produce polished and error-free written material that effectively conveys the intended message to the audience.
    Important: Do not increase the number of words.
    After the blog proofreading is completed, assign a score of either 0 or 1.
    A score of 0 indicates that the blog needs revisions and should not be published.
    Provide feedback to the blogger when the score is 0.

    Blog: {blog}

    Answer: 
    Score: 
    Feedback:"""
)
    blog = blog.replace('"', '')
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    task = proofreading_blog_template.format(blog=blog)
    return llm.invoke(task)
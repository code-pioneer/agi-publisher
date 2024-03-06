from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from mainapp.settings import LLM_MODEL, TOOLS


@tool
def createBlog(topic: str) -> str:
    """Generate a blog for a given topic."""
    print(f'createBlog')
    create_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to write a structured blog post for a given topic.
    Use the guidelines and must have a title:
    
    Title:   

    Guidelines: Start with a compelling hook to grab the reader's attention and briefly introduce the topic's significance. Provide a succinct overview of what the blog post will cover, including the main thesis or argument. Keep it to 100 words.
    
    Divide the body into three paragraphs, each focusing on a specific aspect or subtopic related to the main theme. Use topic sentences to introduce main ideas and support them with evidence or examples. Ensure smooth transitions between paragraphs to maintain coherence. Keep it to 300 words.

    Summarize the main points discussed in the body paragraphs and restate the thesis or main argument. End with a thought-provoking statement or call to action to leave a lasting impression on the reader. Keep it to approximately 100 words.

    Compile a concise list of sources used in the blog post, providing proper attribution and bibliographic details at the end of the post. 
    Remove all quotation marks from the sources.
    Topic: {topic}

    Answer format should be. 
     
    Answer: """
    )
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    task = create_blog_template.format(topic=topic)
    return llm.invoke(task)

TOOLS.append(createBlog)
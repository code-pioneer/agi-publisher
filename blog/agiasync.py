from langchain_core.callbacks import Callbacks
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import tool
import os
from langchain_core.prompts import PromptTemplate
from mainapp.settings import LLM_MODEL
from datetime import datetime
import pprint

chunks = []
prompt = hub.pull("hwchase17/openai-tools-agent")

llm = ChatOpenAI(model=LLM_MODEL, temperature=0, streaming=True)

create_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to write a structured blog post for a given topic.
    Use the guidelines and must have a title:
    
    Title:   

    Guidelines: Start with a compelling hook to grab the reader's attention and briefly introduce the topic's significance. Provide a succinct overview of what the blog post will cover, including the main thesis or argument. Keep it to 100 words.
    
    Divide the body into three paragraphs, each focusing on a specific aspect or subtopic related to the main theme. Use topic sentences to introduce main ideas and support them with evidence or examples. Ensure smooth transitions between paragraphs to maintain coherence. Keep it to 300 words.

    Summarize the main points discussed in the body paragraphs and restate the thesis or main argument. End with a thought-provoking statement or call to action to leave a lasting impression on the reader. Keep it to approximately 100 words.

    Compile a concise list of sources used in the blog post, providing proper attribution and bibliographic details at the end of the post.

    Topic: {topic}

    Answer format should be. 
     
        Answer: """
)

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

        Answer format should be.  
            Answer: 
            Score: 
            Feedback:"""
)

revise_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to review profreading feedback and revise the given blog post.
        
    Blog: {blog}
    Feedback: {feedback}


    Answer format should be. 
     
        Answer: """
)

html_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to convert given Blog in to HTML text for Blog publication:
    Do not ommit any content.  
    Do not include save_to_file in html href.

    Blog: {blog}

    Answer format should be. 
     
        Answer: """
)

md_blog_template = PromptTemplate.from_template(
    """You are an AI language model assistant. Your objective is to convert given Blog in to Mark down text for Blog publication:
    Do not ommit any content.  
    Do not include save_to_file in html href.

    Blog: {blog}

    Answer format should be. 
     
        Answer: """
)

# save_blog_template = PromptTemplate.from_template(
#     """You are an AI language model assistant. Your objective is to save given Blog to desktop:
#     Do not ommit any content.  

#     Blog: {blog}

#     Answer format should be. 
     
#         Answer: """
# )

@tool
async def createBlog(topic: str, callbacks: Callbacks) -> str:
    """Generate a blog for a given topic."""
    print(f'createBlog')
    chain = create_blog_template | llm.with_config(
        {
            "run_name": "Create Blog LLM",
            "tags": ["tool_llm"],
            "callbacks": callbacks,  # <-- Propagate callbacks
        }
    )
    chunks = [chunk async for chunk in chain.astream({"topic": topic})]
    return "".join(chunk.content for chunk in chunks)
   #task = create_blog_template.format(topic=topic)
   # return llm.invoke(task)

@tool
async def proofreadingBlog(blog: str) -> str:
    """Proofread the blog once it's generated."""
    print(f'proofreadingBlog')
    task = proofreading_blog_template.format(blog=blog)
    return llm.invoke(task)

@tool
async def publishBlogHtml(blog: str) -> str:
    """When the blog is ready to be published, convert it to HTML format."""
    #print(f'publishBlogHtml - {blog}')
    task = html_blog_template.format(blog=blog)
    return llm.invoke(task)

@tool
async def publishBlogMD(blog: str) -> str:
    """When the blog is ready to be published, convert it to Markdown format."""
    #print(f'publishBlogMD - {blog}')
    task = md_blog_template.format(blog=blog)
    return llm.invoke(task)
   
@tool
async def reviseBlog(blog: str, feedback: str) -> str:
    """Revise the blog when proofreading is complete and revisions are needed."""
    #print(f'reviseBlog - {feedback}')
    task = revise_blog_template.format(blog=blog, feedback=feedback)
    return llm.invoke(task)

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop') 
 
def save_file(result):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f'blog_{timestamp}'
    file_path = os.path.join(desktop_path, file_name)
    with open(file_path, 'w') as file:
        file.write(result)
        
@tool
async def save_to_file(result: str, ) -> str:
    """Save the final blog post result using the correct file type."""
    print(f'save_to_file')
    return save_file(result)

#tools = [createBlog, proofreadingBlog, reviseBlog, publishBlogHtml, publishBlogMD, save_to_file]
tools = [createBlog]


# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_config({"run_name":"Agent"})

async def blogAgent(topic):
    input = f'Your objective is to perform all required tasks as part of this fullfillment. {topic}'
    result=""
    async for event in agent_executor.astream_events({"input": input},version="v1",):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print(
                    f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                )
        elif kind == "on_chain_end":
            if (
                event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print()
                print("--")
                print(
                    f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                )
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                print(content, end="|")
        elif kind == "on_tool_start":
            print("--")
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")
       
    #result = agent_executor.invoke({"input": input})
    return {'answer' : result}
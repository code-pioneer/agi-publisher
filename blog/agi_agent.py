from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.prompts import PromptTemplate
from mainapp.settings import LLM_MODEL
from blog.agis import create_blog, proof_reading_blog, revise_blog, publish_blog_html, publish_blog_md, save_to_file, generate_filename_extension


def init_agent():
    prompt = hub.pull("hwchase17/openai-tools-agent")
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    tools = [create_blog.createBlog, 
            proof_reading_blog.proofreadingBlog, 
            revise_blog.reviseBlog, 
            publish_blog_html.publishBlogHtml, 
            publish_blog_md.publishBlogMD,
            generate_filename_extension.generate_filename, 
            save_to_file.save_to_file]
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def blogAgent(topic):
    input = f'Your objective is to perform all required tasks as part of this fullfillment. Publishing as HTML or Mark Down. Avoid publishing in both HTML and Mark Down format. Topic: {topic}'
    agent_executor = init_agent()
    result = agent_executor.invoke({"input": input})
    return {'answer' : result['output']}
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain import hub
from mainapp.settings import LLM_MODEL
from blog.agis.tools import agent_tools, tool_profile, tools_profiles
from blog.db import save_blog_response, get_blog_by_id
import json


tools = agent_tools()
tools_profile_list = tools_profiles()
profile_list = ""
for tools_profile in tools_profile_list:
    profile_list = profile_list + " " + tools_profile.get('profile')
print(f"tools_profile={profile_list}")


async def init_agent():
    prompt = hub.pull("hwchase17/openai-tools-agent")
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True).with_config({"run_name":"Agent"})

async def blog_agent(consumer, topic, id):
    print("Blog Agent")
    blog_instance = await get_blog_by_id(id.strip())
    topic = blog_instance.topic
    input = f'Your objective is to perform all required tasks as part of this fullfillment. Topic: {topic}. ID: { blog_instance.id}'
    
    async  def send_message_to_clients(message):    
        await consumer.send(text_data=json.dumps({
                'message': message
        })) 

    result={}     

    agent_executor = await init_agent()
    async for event in agent_executor.astream_events({"input": input},version="v1",):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "Agent"
            ):  
                message = {"profile": tool_profile('organizer'), "message": tool_profile('organizer').get('start_message')}
                await save_blog_response(blog_instance, message)
                await send_message_to_clients(message)
        elif kind == "on_chain_end":
            if (
                event["name"] == "Agent"
            ):  
                message = {"profile": tool_profile('organizer'),"message": tool_profile('organizer').get('end_message')}
                await save_blog_response(blog_instance, message)
                await send_message_to_clients(message)
                await save_blog_response(blog_instance, event['data'].get('output')['output'])

        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="|")
        elif kind == "on_tool_start":
            message = {"profile": tool_profile(event['name']), "message": tool_profile(event['name']).get('start_message')}
            await save_blog_response(blog_instance, message)
            await send_message_to_clients(message)
        elif kind == "on_tool_end":
            message = {"profile": tool_profile(event['name']), "message": tool_profile(event['name']).get('end_message')}
            await save_blog_response(blog_instance, message)
            await send_message_to_clients(message)

            if event['data'].get('output'):
                await save_blog_response(blog_instance, event['data'].get('output'))
                # message1 = {"profile": tool_profile(event['name']), "message": event['data'].get('output')}
                # await send_message_to_clients(message1)
    return {'answer' : result}
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
    step = 0
    message = {"profile": tool_profile('organizer'), "message": tool_profile('organizer').get('start_message')}
    await send_message_to_clients(message)
    result[step] = f"🚀 Blog Generation Started! 🚀" 
    await save_blog_response(blog_instance, result[step])
    message = {"profile": tool_profile('organizer'),"message": result[step]}
    await send_message_to_clients(message)

    agent_executor = await init_agent()
    async for event in agent_executor.astream_events({"input": input},version="v1",):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "Agent"
            ):  
                step+=1
                result[step] = f"Digital assists {tools_profile}' are assigned for your task."
                await save_blog_response(blog_instance, result[step])
        elif kind == "on_chain_end":
            if (
                event["name"] == "Agent"
            ):  
                step+=1
                result[step] = f"🎉 Blog Generation Completed! 🎉"
                await save_blog_response(blog_instance, result[step])
                message2 = {"profile": tool_profile('organizer'),"message": "🎉 Blog Generation Completed! 🎉"}
                result[step] = {"message": "🎉 Blog Generation Completed! 🎉"}
                result[step]['data'] = event['data'].get('output')['output']
                await save_blog_response(blog_instance, result[step]['data'])
                message1 = {"profile": tool_profile('organizer'),"message": result[step]['data']}
                await send_message_to_clients(message1)
                await send_message_to_clients(message2)

        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="|")
        elif kind == "on_tool_start":
            step+=1
            result[step] = f"Digital assistant {tool_profile(event['name'])} is assigned for your task."
            await save_blog_response(blog_instance, result[step])
            message = {"profile": tool_profile(event['name']), "message": tool_profile(event['name']).get('start_message')}

            await send_message_to_clients(message)
        elif kind == "on_tool_end":
            step+=1
            result[step] = f"Digital assistant {tool_profile(event['name'])} has completed the task."
            await save_blog_response(blog_instance, result[step])
            message2 = {"profile": tool_profile(event['name']), "message": tool_profile(event['name']).get('end_message')}
            result[step] = {'message' : f"Digital assistant {tool_profile(event['name'])} has completed the task."}
            result[step]['data'] = event['data'].get('output')

            if result[step]['data']:
                await save_blog_response(blog_instance, result[step]['data'])
                message1 = {"profile": tool_profile(event['name']), "message": event['data'].get('output')}
                await send_message_to_clients(message1)
            await send_message_to_clients(message2)
    return {'answer' : result}
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain import hub
from mainapp.settings import LLM_MODEL
from videos.agis.tools import agent_tools, tool_profile, tools_profiles
from videos.db import save_video_response, get_video_by_id, update_video_request
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

async def video_agent(topic, id, interactive_mode, task_name, task_id):
    print("Video Agent")
    video_instance = await get_video_by_id(id)
    topic = video_instance.topic
    long_video = video_instance.long_video
    theme = video_instance.theme
    voice = video_instance.voice
    image_prompt = video_instance.image_prompt

    params = {"long_video": long_video, "theme": theme, "voice": voice}
    if interactive_mode:
        if task_name == 'prep':
            input = f'''Your objective is to perform following tasks. 
            1. Generate Filename for the topic. 
            2. Update Database with Filename            
            Topic: {topic}. VIDEO_PARAMS: {json.dumps(params)} ID: { video_instance.id} task_id: { task_id} 
            '''
        elif task_name == 'image':
           input = f'''Your objective is to perform following tasks, Do not use any other tools. 
            1. Generate an approriate Image.   
            2. Once image is ready and image_url is available, update Database with image_url.        
            Topic: {image_prompt}. VIDEO_PARAMS: {json.dumps(params)} ID: { video_instance.id} Filename: {video_instance.video_name} task_id: {task_id} video_url: ''  '''
        elif task_name == 'transcript':
            input = f'''Your objective is to perform following tasks, Do not use any other tools.
            1. Generate Filename for the topic. 
            2. Generate transcript for video creation on a given topic.  
            3. Once transcript is ready, update Database with filename and transcript.        
            Topic: {topic}. VIDEO_PARAMS: {json.dumps(params)} ID: { video_instance.id} task_id: { task_id}  '''
        elif task_name == 'video':
            input = f'''Your objective is to perform following tasks, Do not use any other tools. 
            1. Generate Video using image and transcript.  
            2. Once video is ready, update Database with video_url.        
            Topic: {topic}. VIDEO_PARAMS: {json.dumps(params)} ID: { video_instance.id} Filename: {video_instance.video_name}
            image_url: {video_instance.imgurl} transcript: {video_instance.transcript} task_id: { task_id} 
            '''
        elif task_name == 'publish':
            input = f'''Your objective is to perform following tasks, Do not use any other tools. 
            1. Save the final video and transcript result once video is ready
            2. Generate social post content
            3. Once social post is ready, update Database        

            Topic: {topic}. VIDEO_PARAMS: {json.dumps(params)} ID: { video_instance.id} Filename: {video_instance.video_name}
            image_url: {video_instance.imgurl} transcript: {video_instance.transcript} video_url: {video_instance.videourl} task_id: { task_id} 
            '''
        else:
            pass
    else:
        input = f'''Your objective is to perform all required tasks as part of this fullfillment including generating social post in the end. 
            Follow following order while fullfilling the task:
            1. Generate Filename for the topic.
            2. Generate an approriate Image.
            3. Generate transcript for video creation.
            4. Generate Video using image and transcript.
            5. Save the Video transcript result
            6. Generate Social Post content.
            
            Topic: {topic}. VIDEO_PARAMS: {json.dumps(params)} ID: { video_instance.id}'''
            

    result={}     

    agent_executor = await init_agent()
    async for event in agent_executor.astream_events({"input": input},version="v1",):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "Agent"
            ):  
                message = {"profile": tool_profile('organizer'), "message": tool_profile('organizer').get('start_message')}
                await save_video_response(video_instance, message)
                # await send_message_to_clients(message)
        elif kind == "on_chain_end":
            if (
                event["name"] == "Agent"
            ):  
                message = {"profile": tool_profile('organizer'),"message": tool_profile('organizer').get('end_message')}
                await save_video_response(video_instance, message)
                message_data= {"profile": tool_profile('organizer'),"messageData": event['data'].get('output')['output']}
                # await send_message_to_clients(message)
                await save_video_response(video_instance, message_data)
                message = {"profile": tool_profile('organizer'),"message": 'DONE'}
                # await send_message_to_clients(message)
                await save_video_response(video_instance, message)




        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="|")
        elif kind == "on_tool_start":
            message = {"profile": tool_profile(event['name']), "message": tool_profile(event['name']).get('start_message')}
            await save_video_response(video_instance, message)
            # await send_message_to_clients(message)
        elif kind == "on_tool_end":
            message = {"profile": tool_profile(event['name']), "message": tool_profile(event['name']).get('end_message')}
            await save_video_response(video_instance, message)
            # await send_message_to_clients(message)

            if event['data'].get('output'):
                message = {"profile": tool_profile(event['name']),"event":"output", "messageData": event['data'].get('output')}
                await save_video_response(video_instance, message)
                # message1 = {"profile": tool_profile(event['name']), "message": event['data'].get('output')}
                # await send_message_to_clients(message1)
    return {'answer' : result}
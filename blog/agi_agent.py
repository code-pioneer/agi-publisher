from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain import hub
from mainapp.settings import LLM_MODEL
from blog.agis.tools import agent_tools

tools = agent_tools()

def init_agent():
    prompt = hub.pull("hwchase17/openai-tools-agent")
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True).with_config({"run_name":"Agent"})

# def blogAgent(topic):
#     input = f'Your objective is to perform all required tasks as part of this fullfillment. Publishing as HTML or Mark Down. Avoid publishing in both HTML and Mark Down format. Topic: {topic}'
#     agent_executor = init_agent()
#     result = agent_executor.invoke({"input": input})
#     return {'answer' : result['output']}

async def blogAgent(topic):
    input = f'Your objective is to perform all required tasks as part of this fullfillment. {topic}'
    result={}
    agent_executor = init_agent()
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
                result["agent"]=f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
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
            result["tool"]= f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")
            result["final_output"]=f"Tool output was: {event['data'].get('output')}"
    #result = agent_executor.invoke({"input": input})
    return {'answer' : result}
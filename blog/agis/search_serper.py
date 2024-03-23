from langchain.agents import tool
from langchain.agents import AgentType, Tool, initialize_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import OpenAI
from langchain_core.callbacks import Callbacks
from mainapp.settings import STREAMING

@tool
async def searchTopic(topic: str,callbacks: Callbacks) -> str:
    """Perform Google Search for a given topic"""
    print(f'searchTopic')
    search = GoogleSerperAPIWrapper()
    
    return search.run(topic)
    
    
def setup():
    return searchTopic

def profile():
    profile = {
        "name": "search",
        "profile": "Search",
        "task": "Google Search",
        "url": "assets/img/searcher.png",
    }
    return profile
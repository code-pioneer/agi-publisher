from langchain.agents import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.callbacks import Callbacks
from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from mainapp.settings import LLM_MODEL
from asgiref.sync import sync_to_async
import pprint

llm = ChatOpenAI(temperature=0, model=LLM_MODEL)

schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_summary": {"type": "string"},
    },
    "required": ["news_article_title", "news_article_summary"],
}

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke(content)


def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed =  bs_transformer.transform_documents(
        docs, tags_to_extract=["span"]
    )
    
    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    extracted_content=[]
    for item in splits:
        extracted_content.append(extract(schema=schema, content=item.page_content)['text'])
    
    return {"content":extracted_content}

@tool
def searchTopic(topic: str, callbacks: Callbacks) -> str:
    """Perform Google Search for a given topic"""
    print(f'searchTopic')
    search = GoogleSerperAPIWrapper()
    results= search.results(topic)
        
    # Extract 'organic' elements
    organic_elements = results.get("organic", [])
    
    links=[]
    # Print the extracted elements
    for element in organic_elements:
        links.append(element['link'])
    
    return scrape_with_playwright(links, schema=schema)

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
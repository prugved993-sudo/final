from langchain_core.tools import tool
import requests
from tavily import TavilyClient
from bs4 import BeautifulSoup
import os
from rich import print

from dotenv import load_dotenv
load_dotenv()


#Tavily Tool

tavily = TavilyClient(api_key = os.getenv("TAVILY API KEY"))

@tool
def web_search(query : str) -> str:
    """"Search the ewb for recent and reliable information on a topic. returns title,url and snippet"""
    results = tavily.search(query=query,max_results = 3)

    out = []
    for r in results['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n")
    return "\n----\n".join(out)    

print(web_search.invoke("latest news of dharmendr pradhan"))




#BeautifulSoup Tool

def scrape_url(url : str) -> str:
    """scrape and return clean text content from given url for deep reading"""

    try:
        resp = requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(resp.text,"html.parser")

        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator = " ",strip=True)[:3000]
    except Exception as e:
        return f"Could not Scrap URL: {str(e)}"    
    
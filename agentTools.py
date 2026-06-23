from tavily import TavilyClient
from langchain.tools import tool 
import os
from dotenv import load_dotenv
from rich import print
from bs4 import BeautifulSoup
import requests
load_dotenv()



tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# This tool help to gett the relevent news based on given query........
@tool
def webSearch(query : str) -> str:
    """Search the most recent information about given topic and return titles , URLS snippets."""
    response = tavily.search(query=query,max_results=2)
      
    out = []
    for r in response["results"]:
        out.append(
            f"Title : {r['title']} \n URL : {r['url']} \nSnippet : {r['content'][:300]}\n"
        )
    return "\n-----\n".join(out)



#This tool fn use the concept of data scraping using beautisoup library in python that 
# actually help to extract the web info........

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:1000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"



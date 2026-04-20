from config import tavily_key
from state import State
from tavily import TavilyClient
tavily =TavilyClient(api_key = tavily_key) 

def research(state : State):
    print("Searching for the company details in the web ... ")
    results = tavily.search(query = state["job_url"] , max_results = 5 )
    return {"researched_info" : results}

from pydantic import BaseModel, Field
from tavily import TavilyClient
from config import TAVILY_API_KEY
from langchain_core.messages import SystemMessage, HumanMessage
from config import GROQ_MODEL
from langchain.groq import ChatGroq

class ResearcherConfig(BaseModel):
    researched_summary: str = Field(description="A concise 3-4 sentence of summary of the job description, company background, and any relevant information gathered during research.")
    researched_news: list[str] = Field(description="A list of 3-5 recent news articles, press releases, or any relevant information about the company or industry that may be useful for tailoring the resume and cover letter.")


def search_company(job_url: str , job_description: str) -> str:
    client = TavilyClient(api_key=TAVILY_API_KEY)
    company_search = client.search(
        query = f"company info about {job_url} ",
        max_results=3
    )
    news_search = client.search(
        query = f"recent news about {job_url} ",
        max_results=5
    )
    raw_results = []
    for result in company_search["results"]:
        raw_results.append(f"Company Info: {result['title']}: {result['content']}")

    for result in news_search["results"]:
        raw_results.append(f"Recent News: {result['title']}: {result['content']}")

    return "\n".join(raw_results)


def run_researcher(raw_context: str, job_description: str) -> str:
    llm = ChatGroq(GROQ_MODEL , temperature=0.0)
    structured_llm  = llm.with_structured_output(ResearcherConfig)
    
    messages = [
        SystemMessage(content="""You are a company research specialist.
Given raw search results and a job description, extract and summarize:
1. What the company does, their mission, size, and tech stack
2. Recent notable news about the company

Be factual. Only use information present in the search results."""),
        HumanMessage(content=f"""
JOB DESCRIPTION:
{job_description}

RAW SEARCH RESULTS:
{raw_context}

Extract the company summary and recent news from these results.
""")
    ]
    return structured_llm.invoke(messages)




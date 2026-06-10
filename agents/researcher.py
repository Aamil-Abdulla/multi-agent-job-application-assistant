from pydantic import BaseModel, Field
from tavily import TavilyClient
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from config import GROQ_MODEL, TAVILY_API_KEY
from state import State


class ResearcherOutput(BaseModel):
    researched_summary: str = Field(
        description="A concise 3-4 sentence summary of the company, what they do, their mission, and tech stack if available"
    )
    researched_news: list[str] = Field(
        description="List of 3-5 recent news items about the company, each as a single sentence"
    )


def search_company(job_url: str) -> str:
    client = TavilyClient(api_key=TAVILY_API_KEY)

    company_search = client.search(
        query=f"company info about {job_url}",
        max_results=3
    )
    news_search = client.search(
        query=f"recent news about {job_url} 2025 2026",
        max_results=5
    )

    raw_results = []
    for result in company_search["results"]:
        raw_results.append(f"Company Info: {result['title']}: {result['content']}")
    for result in news_search["results"]:
        raw_results.append(f"Recent News: {result['title']}: {result['content']}")

    if not raw_results:
        return "NO_DATA_FOUND"

    return "\n".join(raw_results)


def run_researcher(raw_context: str, job_description: str) -> ResearcherOutput:
    llm = ChatGroq(model=GROQ_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(ResearcherOutput)

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


def researcher_node(state: State) -> dict:
    print("----- Researcher Agent -----")

    job_description = state.get("job_description", "").strip()
    if not job_description:
        job_description = "No job description provided."

    raw_context = search_company(job_url=state["job_url"])

    if raw_context == "NO_DATA_FOUND":
        return {
            "job_description": job_description,
            "researched_summary": "No company data found.",
            "researched_news": []
        }

    result = run_researcher(raw_context=raw_context, job_description=job_description)

    return {
        "job_description": job_description,
        "researched_summary": result.researched_summary,
        "researched_news": result.researched_news,
    }
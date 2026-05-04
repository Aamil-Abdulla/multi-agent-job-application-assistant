from typing import TypedDict

class State(TypedDict):
    job_url: str
    job_description: str
    company_background: str
    researched_summary: str
    researched_news: list[str]
    analyzed_requirements: str
    analyzed_keywords: list[str]
    written_resume: str
    written_letter: str
    critique: str
    score: int
    suggestions: list[str]
    loops: int
from pydantic import BaseModel, Field
from state import State
from langchain_core.messages import HumanMessage, SystemMessage
from config import GROQ_MODEL
from langchain_groq import ChatGroq


class WriterOutput(BaseModel):
    written_resume: str = Field(
        description="Concise tailored resume bullet points based on the job description, requirements, and keywords"
    )
    written_letter: str = Field(
        description="A concise cover letter highlighting why the candidate fits the role, using keywords from the JD"
    )


def written(job_description: str, analyzed_requirements: str, analyzed_keywords: list[str], background: str) -> WriterOutput:
    llm = ChatGroq(model=GROQ_MODEL, temperature=0)
    llm_structured_output = llm.with_structured_output(WriterOutput)
    llm_messages = [
        SystemMessage(content="You are a professional resume and cover letter writer. Write tailored, concise content based strictly on the job description, analyzed requirements, keywords, and candidate background provided."),
        HumanMessage(content=f"""
CANDIDATE BACKGROUND:
{background}

JOB DESCRIPTION:
{job_description}

ANALYZED REQUIREMENTS:
{analyzed_requirements}

ANALYZED KEYWORDS:
{analyzed_keywords}

Write the best possible resume bullets and cover letter based on the above.
""")
    ]
    return llm_structured_output.invoke(llm_messages)


def run_writer(state: State) -> dict:
    print("----- Writer Agent -----")
    written_output = written(
        job_description=state["job_description"],
        analyzed_requirements=state["analyzed_requirements"],
        analyzed_keywords=state["analyzed_keywords"],
        background=state["background"]
    )
    return {
        "written_resume": written_output.written_resume,
        "written_letter": written_output.written_letter
    }
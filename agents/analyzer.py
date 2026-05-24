## pydantic function -> core function  ->  node function
from pydantic import BaseModel , Field
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from state import State
from config import GROQ_MODEL
class AnalyzerOutput(BaseModel):
    analyzed_requirements : str = Field(
        description="A concise description of the requirements that are analyzed by the analyzer about the job ."
    )
    analyzed_keywords : list[str] = Field(
        description="A list of importtant keywords that are relevant for the job description .These keywords are used for the resume and the cover letter later."
        )
    
def analyzed(job_desctiption : str) -> AnalyzerOutput:
    llm = ChatGroq(model= GROQ_MODEL , temperature = 0)
    structured_output = llm.with_structured_output(AnalyzerOutput)
    llm_messages = [
        SystemMessage(content = " you are a job description analyst. Your role is to analyze the job requirements as well as extract important keywords that are relevant for the job description. These keywords will be used for the resume and the cover letter later. Be concise and factual. Only use information present in the job description."),
        HumanMessage(content = f"""
                     JOB DESCRIPTION:
                     {job_desctiption}
Give me a concise description of the requirement from the job descruption as well as give me the best keywords regarding to the job description only and it should be in the format of the AnalyzerOutput pydantic model .
                     """)
    ]
    return structured_output.invoke(llm_messages)


def run_analyzer(state: State) -> dict:
    analyzed_output = analyzed(state["job_description"])
    return {
        "analyzed_requirements" : analyzed_output.analyzed_requirements,
        "analyzed_keywords" : analyzed_output.analyzed_keywords

    }


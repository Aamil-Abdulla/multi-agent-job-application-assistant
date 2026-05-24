from pydantic import BaseModel, Field
from state import State
from langchain_core.messages import HumanMessage, SystemMessage
from config import GROQ_MODEL
from langchain_groq import ChatGroq

#pydantic -> core agent - > node function


class WriterOutput(BaseModel):
    written_resume : str = Field(
        description="a consice and best reusume content is written with the help of analyzed requirements and key words given"
    )
    written_letter : str = Field(
        description= "A written cover letter content from the job description highlighting why i need this job and also using keywords as well.Make it concise and to the point"
    )

def written(job_description : str , analyzed_requirements : str , analyzed_keywords : list[str]) -> WriterOutput:
    llm = ChatGroq( model = GROQ_MODEL , temperature = 0)
    llm_structured_output = llm.with_structured_output(WriterOutput)
    llm_messages = [
        SystemMessage(content = "You are a pro writer that writes resume and cover letter.your role is to write the best possible and then the cover letter and content for resume is based on job description and as welll as the analyzed requirements and keywords . Be concise and factual. Only use information present in the job description as well as the analyzed requirements and keywords ."),
        HumanMessage(content=f"""
                     JOB_DESCRIPTION:
                     {job_description}
                     ANALYZED_REQUIREMENTS:
                     {analyzed_requirements}
                     ANALYZED_KEYWORDS:
                     {analyzed_keywords}
                        Give me the best possible resume content as well as cover letter content for the job description based on the analyzed requirements and keywords and it should be in the format of the WriterOutput pydantic model .
    """)
    ]
    return llm_structured_output.invoke(llm_messages)

def run_writer(state: State) -> dict:
    written_output = written(state["job_description"], state["analyzed_requirements"], state["analyzed_keywords"])
    return {
        "written_resume": written_output.written_resume,
        "written_letter": written_output.written_letter
    }
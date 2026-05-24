from pydantic import BaseModel , Field
from langchain_core.messages import HumanMessage , SystemMessage
from langchain_groq import ChatGroq
from state import State
from config import GROQ_MODEL
class CriticOutput(BaseModel):
    critique : str = Field(
        description = " a concise critique of the resume and cover letter indicating the weakness of areas and strengths and how it can be imporved "
    )
    score : int = Field(
        description="score from 1 to 10 indicating how good the resume and the cover letter is for the job description. 10 is being the best and 1 the worst"
    )
    suggestions : list[str] = Field(
        description = "list of suggestions indicating how to improve the resume and the cover letter based on job description and the analyzed requirements and keywords . Be concise and factual. Only use information present in the job description as well as the analyzed requirements and keywords ." 
    )


def critique_checker(job_description : str , analyzed_requirements : str , analyzed_keywords : list[str] , written_resume : str , written_letter : str):
    llm = ChatGroq(model = GROQ_MODEL, temperature = 0)
    structured_output = llm.with_structured_output(CriticOutput)
    llm_messages= [
        SystemMessage(content = "You are a job description critic. Find the weakness and strength of the resume and the cover letter based on the job description as well as the analyzed requirements and keywords. Give a score from 1 to 10 indicating how good the resume and the cover letter is for the job description. 10 is being the best and 1 the worst. Also give a concise critique of the resume and cover letter indicating the weakness of areas and strengths and how it can be imporved . Be concise and factual. Only use information present in the job description as well as the analyzed requirements and keywords.")
    ,
    HumanMessage(content= f"""
                 JOB DESCRIPTION:
                 {job_description}
                 ANALYZED_DESCRIPTION:
                 {analyzed_requirements}
                 ANALYZED_KEYWORDS:
                 {analyzed_keywords}
                 WRITTEN_RESUME:
                 {written_resume}
                 WRITTEN_LETTER:
                 {written_letter}
                    Give me a concise critique of the resume and cover letter indicating the weakness of areas and strengths and how it can be imporved as well as give a score from 1 to 10 indicating how good the resume and the cover letter is for the job description. 10 is being the best and 1 the worst and it should be in the format of the CriticOutput pydantic model .   
                    """
    )
    ]
    return structured_output.invoke(llm_messages)


def run_critics(state : State) -> dict:
    critic_output = critique_checker(state["job_description"], state["analyzed_requirements"], state["analyzed_keywords"], state["written_resume"], state["written_letter"])
    return  {
        "critique" : critic_output.critique,
        "score" : critic_output.score,
        "suggestions" : critic_output.suggestions
    }
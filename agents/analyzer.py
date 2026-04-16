os.environ()
from tavily import tavily
search=tavily()



class analyzer(job_url,job_description):
    prompt="""
    {}
you are an AI expert Analyzer agent that analyze using job url and job description.
"""
f'user: "ai analyzer", content : {"job_url"} , {"job_description"}



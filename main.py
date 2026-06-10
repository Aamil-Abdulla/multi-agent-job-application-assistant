from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from datetime import datetime

from graph import build_graph

app = FastAPI(title="Multi-Agent Job Application Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HISTORY_FILE = "history.json"
graph = build_graph()


class JobRequest(BaseModel):
    job_url: str
    job_description: str
    background: str


def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_to_history(entry: dict):
    history = load_history()
    history.insert(0, entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.post("/generate")
async def generate(request: JobRequest):
    try:
        initial_state = {
            "job_url": request.job_url,
            "background": request.background,
            "job_description": request.job_description,
            "company_background": "",
            "researched_summary": "",
            "researched_news": [],
            "analyzed_requirements": "",
            "analyzed_keywords": [],
            "written_resume": "",
            "written_letter": "",
            "critique": "",
            "score": 0,
            "suggestions": [],
            "loops": 0,
        }

        result = await graph.ainvoke(initial_state)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "job_url": request.job_url,
            "researched_summary": result.get("researched_summary", ""),
            "researched_news": result.get("researched_news", []),
            "analyzed_requirements": result.get("analyzed_requirements", ""),
            "analyzed_keywords": result.get("analyzed_keywords", []),
            "written_resume": result.get("written_resume", ""),
            "written_letter": result.get("written_letter", ""),
            "critique": result.get("critique", ""),
            "score": result.get("score", 0),
            "suggestions": result.get("suggestions", []),
        }

        save_to_history(entry)
        return {"status": "success", **entry}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history():
    return load_history()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
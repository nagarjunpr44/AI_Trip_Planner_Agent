from fastapi import FastAPI
from pydantic import BaseModel
from backend.nodes.graph import build_graph
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="AI Travel Planner")
graph = build_graph() 
class Userquery(BaseModel):
    user_question:str

class AnswerResponse(BaseModel):
    final_answer:str


@app.get("/")
def read_root():
    return {"message": "AI Travel Planner API is running. Use POST /ask to query."}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all origins. Later restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask",response_model=AnswerResponse)
def ask_question(query:Userquery):
    state = {
        "messages": [{"role": "user", "content": query.user_question}],
        "user_question": query.user_question,
        "trip_request": None,
        "google_results": None,
        "bing_results": None,
        "reddit_results": None,
        "selected_reddit_urls": None,
        "reddit_post_data": None,
        "google_analysis": None,
        "bing_analysis": None,
        "reddit_analysis": None,
        "final_answer": None
    }

    final_state=graph.invoke(state)

    return {"final_answer":final_state.get("final_answer")}

from dotenv import load_dotenv
from typing import Annotated,List
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing import TypedDict
from backend.models.trip_request import Triprequest,RedditURLAnalysis
from pydantic import BaseModel,Field
from backend.data_sources.web_operations import serp_search,reddit_search_api,reddit_post_retrieval
from backend.agent.llm_wrapper import handle_extract_trip_parameters,google_search_api,bing_search_api
from backend.agent.prompts import (
                     get_reddit_analysis_messages,
                     get_google_analysis_messages,
                     get_bing_analysis_messages,
                     get_reddit_url_analysis_messages,
                     get_synthesis_messages
)
load_dotenv()
llm=init_chat_model("gpt-4.1-2025-04-14")

class State(TypedDict):
    messages:Annotated[list,add_messages]
    user_question: str
    trip_request:Triprequest|None
    google_results:str|None
    bing_results:str|None
    reddit_results:str|None
    selected_reddit_urls:list[str]|None
    reddit_post_data:list|None
    google_analysis: str|None
    bing_analysis:str|None
    reddit_analysis:str|None
    final_answer:str|None


def extract_trip_parameters(state: State):
    user_question=state.get("user_question","")
    trip_request=handle_extract_trip_parameters(user_question)

    return {"trip_request": trip_request}

def google_search(state:State):
    trip_request=state.get("trip_request")

    if trip_request:
        search_query=f"Trip to {trip_request.destination},activities:{','.join(trip_request.activities)},interests:{','.join(trip_request.interests)}"
    else:
        search_query=state.get("user_question","")

    print(f"Searching Google for :{search_query}")
    
    google_results=google_search_api(search_query)
    
    return {"google_results":google_results}

    
def bing_search(state:State):
    trip_request=state.get("trip_request")

    if trip_request:
        search_query=f"Trip to {trip_request.destination},activities:{','.join(trip_request.activities)},interests:{','.join(trip_request.interests)}"
    else:
        search_query=state.get("user_question","")

    print(f"Searching Bing for :{search_query}")
    
    bing_results=bing_search_api(search_query)

    return {"bing_results":bing_results}

def reddit_search(state:State):
    trip_request=state.get("trip_request")

    if trip_request:
        search_query=f"Trip to {trip_request.destination},activities:{','.join(trip_request.activities)},interests:{','.join(trip_request.interests)}"
    else:
        search_query=state.get("user_question","")

    print(f"Searching Reddit for :{search_query}")

    reddit_results=reddit_search_api(search_query)

    print(reddit_results)

    return {"reddit_results":reddit_results}

def analyze_reddit_posts(state:State):
    user_question=state.get("user_question")
    reddit_results=state.get("reddit_results","")

    if not reddit_results:
        return {"selected_reddit_urls":[]}
    
    structured_llm=llm.with_structured_output(RedditURLAnalysis)
    messages=get_reddit_url_analysis_messages(user_question,reddit_results)

    try:
        analysis = structured_llm.invoke(messages)
        selected_urls = analysis.selected_urls

        print("Selected URLs:")
        for i, url in enumerate(selected_urls, 1):
            print(f"   {i}. {url}")

    except Exception as e:
        print(e)
        selected_urls = []

    return {"selected_reddit_urls": selected_urls}

def retrieve_reddit_posts(state:State):
    print("Getting reddit post comments")

    selected_urls = state.get("selected_reddit_urls", [])

    if not selected_urls:
        return {"reddit_post_data": []}

    print(f"Processing {len(selected_urls)} Reddit URLs")

    reddit_post_data = reddit_post_retrieval(selected_urls)

    if reddit_post_data:
        print(f"Successfully got {len(reddit_post_data)} posts")
    else:
        print("Failed to get post data")
        reddit_post_data = []

    print(reddit_post_data)
    return {"reddit_post_data": reddit_post_data}


def analyze_google_results(state:State):
    print("Analyzing google search results")

    trip_request=state.get("trip_request")
    if trip_request:
        search_context=f"Trip to {trip_request.destination},activities:{','.join(trip_request.activities)},interests:{','.join(trip_request.interests)}"
    else:
        search_context=state.get("user_question","")
    google_results = state.get("google_results", "")

    messages = get_google_analysis_messages(search_context, google_results,trip_request)
    reply = llm.invoke(messages)

    return {"google_analysis": reply.content}


def analyze_bing_results(state:State):
    print("Analyzing bing search results")

    trip_request=state.get("trip_request")
    if trip_request:
        search_context=f"Trip to {trip_request.destination},activities:{','.join(trip_request.activities)},interests:{','.join(trip_request.interests)}"
    else:
        search_context=state.get("user_question","")
    bing_results = state.get("bing_results", "")

    messages = get_bing_analysis_messages(search_context, bing_results,trip_request)
    reply = llm.invoke(messages)

    return {"bing_analysis": reply.content}
    

def analyze_reddit_results(state:State):
    print("Analyzing reddit search results")

    trip_request=state.get("trip_request")
    if trip_request:
        search_context=f"Trip to {trip_request.destination},activities:{','.join(trip_request.activities)},interests:{','.join(trip_request.interests)}"
    else:
        search_context=state.get("user_question","")
    reddit_results = state.get("reddit_results", "")
    reddit_post_data = state.get("reddit_post_data", "")

    messages = get_reddit_analysis_messages(search_context, reddit_results, reddit_post_data,trip_request)
    reply = llm.invoke(messages)

    return {"reddit_analysis": reply.content}
    

def synthesize_analyses(state:State):
    print("Combine all results together")

    trip_request=state.get("trip_request")

    if trip_request:
        search_context=f"Trip to {trip_request.destination},activities:{','.join(trip_request.activities)},interests:{','.join(trip_request.interests)}"
    else:
        search_context=state.get("user_question","")

    google_analysis = state.get("google_analysis", "")
    bing_analysis = state.get("bing_analysis", "")
    reddit_analysis = state.get("reddit_analysis", "")

    messages = get_synthesis_messages(
        search_context, google_analysis, bing_analysis, reddit_analysis
    )

    reply = llm.invoke(messages)
    final_answer = reply.content

    return {"final_answer": final_answer, "messages": [{"role": "assistant", "content": final_answer}]}

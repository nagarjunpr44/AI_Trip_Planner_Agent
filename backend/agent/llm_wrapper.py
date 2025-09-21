from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from backend.models.trip_request import Triprequest,RedditURLAnalysis
from backend.data_sources.web_operations import serp_search,reddit_search_api,reddit_post_retrieval
from backend.agent.prompts import (get_trip_request_messages,
                     get_reddit_analysis_messages,
                     get_google_analysis_messages,
                     get_bing_analysis_messages,
                     get_reddit_url_analysis_messages,
                     get_synthesis_messages
)
load_dotenv()

llm=init_chat_model("gpt-4.1-2025-04-14")



def handle_extract_trip_parameters(user_question:str):
    
    if not user_question:
        return{"trip_request":None}
    
    messages=get_trip_request_messages(user_question)
    structured_llm=llm.with_structured_output(Triprequest)

    try:
        trip_request=structured_llm.invoke(messages)
        return trip_request
    except Exception as e:
        print(f"Failed to parse trip request:{e}")
        return None


def google_search_api(query:str):
    """Perform Google search using Bright Data API."""
    if not query:
        return None
    results=serp_search(query,engine="google")

    return results

def bing_search_api(query:str):
    """Perform bing search using Bright Data API."""
    if not query:
        return None
    results=serp_search(query,engine="bing")

    return results


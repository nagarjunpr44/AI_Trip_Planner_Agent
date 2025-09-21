from dotenv import load_dotenv
from backend.nodes.graph import build_graph

load_dotenv()
graph = build_graph()

def run_chatbot():
    print("AI-Agent Travel Planner")
    print("Type 'exit' to quit\n")

    while True:
        user_input=input("Ask me anything: ")
        if user_input.lower()=="exit":
            print("Bye......")
            break
        
        state={
            "messages":[{"role":"user","content":user_input}],
            "user_question":user_input,
            "trip_request":None,
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

        print("\n Starting Parallel research process...")
        print("\n Launching Google, Bing, and Reddit seaches ....\n")
        final_state=graph.invoke(state)

        if final_state.get("final_answer"):
            print(f"\n Final Answer:\n{final_state.get('final_answer')}\n")

        print("-"* 80)

if __name__=="__main__":
    run_chatbot()

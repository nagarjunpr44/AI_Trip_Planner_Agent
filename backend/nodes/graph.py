from langgraph.graph import StateGraph, START, END
from backend.nodes.node_functions import (
    State,
    extract_trip_parameters,
    google_search,
    bing_search,
    reddit_search,
    analyze_reddit_posts,
    retrieve_reddit_posts,
    analyze_google_results,
    analyze_bing_results,
    analyze_reddit_results,
    synthesize_analyses
)


def build_graph():
    graph_builder = StateGraph(State)

    # Add nodes
    graph_builder.add_node("extract_trip_parameters", extract_trip_parameters)
    graph_builder.add_node("google_search", google_search)
    graph_builder.add_node("bing_search", bing_search)
    graph_builder.add_node("reddit_search", reddit_search)
    graph_builder.add_node("analyze_reddit_posts", analyze_reddit_posts)
    graph_builder.add_node("retrieve_reddit_posts", retrieve_reddit_posts)
    graph_builder.add_node("analyze_google_results", analyze_google_results)
    graph_builder.add_node("analyze_bing_results", analyze_bing_results)
    graph_builder.add_node("analyze_reddit_results", analyze_reddit_results)
    graph_builder.add_node("synthesize_analyses", synthesize_analyses)

    # Add edges
    graph_builder.add_edge(START, "extract_trip_parameters")
    graph_builder.add_edge("extract_trip_parameters", "google_search")
    graph_builder.add_edge("extract_trip_parameters", "bing_search")
    graph_builder.add_edge("extract_trip_parameters", "reddit_search")
    graph_builder.add_edge("google_search", "analyze_reddit_posts")
    graph_builder.add_edge("bing_search", "analyze_reddit_posts")
    graph_builder.add_edge("reddit_search", "analyze_reddit_posts")
    graph_builder.add_edge("analyze_reddit_posts", "retrieve_reddit_posts")
    graph_builder.add_edge("retrieve_reddit_posts", "analyze_reddit_results")
    graph_builder.add_edge("retrieve_reddit_posts", "analyze_google_results")
    graph_builder.add_edge("retrieve_reddit_posts", "analyze_bing_results")
    graph_builder.add_edge("analyze_google_results", "synthesize_analyses")
    graph_builder.add_edge("analyze_bing_results", "synthesize_analyses")
    graph_builder.add_edge("analyze_reddit_results", "synthesize_analyses")
    graph_builder.add_edge("synthesize_analyses", END)

    return graph_builder.compile()
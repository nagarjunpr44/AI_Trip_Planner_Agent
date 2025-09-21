from typing import Dict, Any
from backend.models.trip_request import Triprequest


class PromptTemplates:
    """Container for all prompt templates used in the research assistant."""

    @staticmethod
    def reddit_url_analysis_system() -> str:
        """System prompt for analyzing Reddit URLs."""
        return """You are an expert at analyzing social media content. Your task is to examine Reddit search results and identify the most relevant posts that would provide valuable additional information for answering the user's question.

Analyze the provided Reddit results and identify URLs of posts that contain valuable information worth investigating further. Focus on posts that:
- Directly relate to the user's question
- Contain detailed discussions or expert opinions
- Have high engagement (upvotes/comments)
- Provide unique perspectives or insights

Return a structured response with the selected URLs."""

    @staticmethod
    def reddit_url_analysis_user(user_question: str, reddit_results: str,trip_request:"Triprequest | None"=None) -> str:
        """User prompt for analyzing Reddit search results."""
        trip_info=f"\n Trip Request Details:{trip_request}"if trip_request else ""
        return f"""Question: {user_question}{trip_info}

Reddit Results: {reddit_results}

Please analyze these Reddit results and identify the most valuable posts for answering the user's question."""

    @staticmethod
    def google_analysis_system() -> str:
        """System prompt for analyzing Google search results."""
        return """You are an expert research analyst. Analyze the provided Google search results to extract key insights that answer the user's question.

Focus on:
- Main factual information and authoritative sources
- Official websites, documentation, and reliable sources
- Key statistics, dates, and verified information
- Any conflicting information from different sources

Provide a concise analysis highlighting the most relevant findings."""

    @staticmethod
    def google_analysis_user(user_question: str, google_results: str,trip_request:"Triprequest | None"=None) -> str:
        """User prompt for analyzing Google search results."""
        trip_info=f"\n Trip Request Details:{trip_request}"if trip_request else ""
        return f"""Question: {user_question}{trip_info}


    Google Search Results: {google_results}

    Based on this information, provide actionable insights for planning a trip. Include:
    - Recommended places to visit
    - Popular activities related to the user's interests
    - Any relevant travel tips or considerations
    - Summarize conflicting information or choices

    Use a clear, structured format for easy reading."""

    @staticmethod
    def bing_analysis_system() -> str:
        """System prompt for analyzing Bing search results."""
        return """You are an expert research analyst. Analyze the provided Bing search results to extract complementary insights that answer the user's question.

Focus on:
- Additional perspectives not covered in other sources
- Technical details and documentation
- News articles and recent developments
- Microsoft ecosystem and enterprise perspectives

Provide a concise analysis highlighting unique findings and perspectives."""

    @staticmethod
    def bing_analysis_user(user_question: str, bing_results: str,trip_request:"Triprequest | None"=None) -> str:
        """User prompt for analyzing Bing search results."""
        trip_info=f"\n Trip Request Details:{trip_request}"if trip_request else ""
        return f"""Question: {user_question}{trip_info}

Bing Search Results: {bing_results}

Please analyze these Bing results and extract insights that complement other search sources."""

    @staticmethod
    def reddit_analysis_system() -> str:
        """System prompt for analyzing Reddit discussions."""
        return """You are a travel research expert analyzing social media discussions. Extract insights that help a user plan a trip.

    Focus on:
    - Community experiences and tips
    - Recommended activities and places
    - Warnings or pitfalls mentioned by users
    - Popular or highly-upvoted opinions
    - Provide information in a structured, clear format

    IMPORTANT: When referencing specific content, directly quote it and mention the subreddit or context.
    Highlight both positive and negative experiences, controversies, and varying opinions."""

    @staticmethod
    def reddit_analysis_user(
        user_question: str, reddit_results: str, reddit_post_data: list,trip_request:"Triprequest | None"=None
    ) -> str:
        """User prompt for analyzing Reddit discussions."""
        trip_info=f"\n Trip Request Details:{trip_request}"if trip_request else ""
        return f"""Question: {user_question}{trip_info}

Reddit Search Results: {reddit_results}

Detailed Reddit Post Data: {reddit_post_data}

Please analyze this Reddit content and extract community insights, user experiences, and relevant discussions."""

    @staticmethod
    def synthesis_system() -> str:
        """System prompt for synthesizing all analyses."""
        return """You are an expert research synthesizer. Combine the provided analyses from different sources to create a comprehensive, well-structured answer.

Your task:
- Synthesize insights from Google, Bing, and Reddit analyses
- Identify common themes and conflicting information
- Present a balanced view incorporating different perspectives
- Structure the response logically with clear sections
- Cite the source type (Google, Bing, Reddit) for key claims
- Highlight any contradictions or uncertainties

Create a comprehensive answer that addresses the user's question from multiple angles.

"""

    @staticmethod
    def synthesis_user(
        user_question: str,
        google_analysis: str,
        bing_analysis: str,
        reddit_analysis: str,
        trip_request:"Triprequest | None"=None
    ) -> str:
        """User prompt for synthesizing all analyses."""
        trip_info=f"\n Trip Request Details:{trip_request}"if trip_request else ""

        return f"""Question: {user_question}{trip_info}

    Google Analysis: {google_analysis}

    Bing Analysis: {bing_analysis}

    Reddit Community Analysis: {reddit_analysis}

    Synthesize these analyses into a comprehensive trip plan:
    - Highlight recommended destinations, activities, and interests
    - Include pros/cons or conflicting opinions
    - Present the answer in a structured, readable format
    - Use clear sections for each source if needed

    """

    
    @staticmethod
    def trip_request_system() -> str:
        """System prompt for extracting trip request details."""
        return (
            "You are an expert travel planner and data extractor. "
            "Your task is to carefully read the user's input and extract the following structured information:\n"
            "1. destination: The city, country, or region the user wants to visit.\n"
            "2. days: Number of days for the trip.\n"
            "3. budget: Total budget in numeric form if mentioned; otherwise return null.\n"
            "4. interests: List of user interests or travel preferences (e.g., food, adventure, museums, beaches). "
            "If not mentioned, return an empty list.\n\n"
            "Return the result strictly in JSON format matching this structure:\n"
            "{'destination': str | None, 'days': int | None, 'budget': float | None, 'interests': list[str]}"
        )

    @staticmethod
    def trip_request_user(user_input: str) -> str:
        """User prompt for extracting trip request details."""
        return f"User Input: {user_input}"

        


def create_message_pair(system_prompt: str, user_prompt: str) -> list[Dict[str, Any]]:
    """
    Create a standardized message pair for LLM interactions.

    Args:
        system_prompt: The system message content
        user_prompt: The user message content

    Returns:
        List containing system and user message dictionaries
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


# Convenience functions for creating complete message arrays
def get_trip_request_messages(user_input: str) -> list[Dict[str, Any]]:
    """Create system and user messages for TripRequest extraction."""
    return create_message_pair(
        PromptTemplates.trip_request_system(),
        PromptTemplates.trip_request_user(user_input)
    )



def get_reddit_url_analysis_messages(
    user_question: str, reddit_results: str) -> list[Dict[str, Any]]:
    """Get messages for Reddit URL analysis."""
    return create_message_pair(
        PromptTemplates.reddit_url_analysis_system(),
        PromptTemplates.reddit_url_analysis_user(user_question, reddit_results),
    )


def get_google_analysis_messages(
    user_question: str, google_results: str,trip_request:"Triprequest |None"=None
) -> list[Dict[str, Any]]:
    """Get messages for Google results analysis."""
    return create_message_pair(
        PromptTemplates.google_analysis_system(),
        PromptTemplates.google_analysis_user(user_question, google_results,trip_request),
    )


def get_bing_analysis_messages(
    user_question: str, bing_results: str,trip_request:"Triprequest |None"=None
) -> list[Dict[str, Any]]:
    """Get messages for Bing results analysis."""
    return create_message_pair(
        PromptTemplates.bing_analysis_system(),
        PromptTemplates.bing_analysis_user(user_question, bing_results,trip_request),
    )


def get_reddit_analysis_messages(
    user_question: str, reddit_results: str, reddit_post_data: list,trip_request:"Triprequest |None"=None
) -> list[Dict[str, Any]]:
    """Get messages for Reddit discussions analysis."""
    return create_message_pair(
        PromptTemplates.reddit_analysis_system(),
        PromptTemplates.reddit_analysis_user(
            user_question, reddit_results, reddit_post_data,trip_request
        ),
    )


def get_synthesis_messages(
    user_question: str, google_analysis: str, bing_analysis: str, reddit_analysis: str,trip_request:"Triprequest |None"=None
) -> list[Dict[str, Any]]:
    """Get messages for final synthesis."""
    return create_message_pair(
        PromptTemplates.synthesis_system(),
        PromptTemplates.synthesis_user(
            user_question, google_analysis, bing_analysis, reddit_analysis,trip_request
        ),
    )
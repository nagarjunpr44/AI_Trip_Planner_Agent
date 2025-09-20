# Multi research AI agent

A sophisticated multi-agent research system that leverages multiple search engines and AI analysis to provide comprehensive answers to user queries. The system performs parallel searches across Google, Bing, and Reddit, then uses AI to analyze and synthesize the results into a coherent response.

## 🌟 Features

- **Multi-Source Research**: Simultaneously searches Google, Bing, and Reddit for comprehensive information gathering
- **AI-Powered Analysis**: Uses GPT-4 to analyze search results from each source
- **Reddit Deep-Dive**: Intelligently selects relevant Reddit URLs and retrieves post comments for detailed insights
- **Parallel Processing**: Executes multiple search operations concurrently for faster results
- **Synthesis Engine**: Combines analyses from all sources into a unified, coherent answer
- **Interactive Chat Interface**: Simple command-line interface for asking questions

## 🏗️ Architecture

The system is built using LangGraph and follows a state-based workflow:

```
START
├── Google Search
├── Bing Search 
└── Reddit Search
    ↓
Reddit URL Analysis
    ↓
Reddit Post Retrieval
    ↓
┌── Google Analysis
├── Bing Analysis
└── Reddit Analysis
    ↓
Final Synthesis
    ↓
END
```

## 🔧 Components

### Core Modules
- **main.py**: Main orchestration logic and graph definition
- **web_operations.py**: Search API integrations (Google, Bing, Reddit)
- **prompts.py**: AI prompt templates for different analysis stages

### Key Functions
- `google_search()` / `bing_search()`: Perform web searches using SERP API
- `reddit_search()`: Search Reddit for relevant discussions
- `analyze_reddit_posts()`: AI-powered selection of valuable Reddit URLs
- `retrieve_reddit_posts()`: Extract detailed post and comment data
- `analyze_*_results()`: Individual analysis for each search source
- `synthesize_analyses()`: Combine all analyses into final answer

## 📋 Prerequisites

- Python 3.10+
- OpenAI API key
- Bright data API key (for Google/Bing/reddit searches)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nagarjunpr44/Multi-research-agent.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   SERP_API_KEY=your_serp_api_key
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=your_reddit_user_agent
   ```

## 📦 Dependencies

```
langgraph
langchain
openai
python-dotenv
pydantic
requests
```

## 💻 Usage

1. **Start the chatbot**
   ```bash
   python main.py
   ```

2. **Ask questions**
   ```
   Ask me anything: What are the currently llms used for?
   ```

3. **Exit the application**
   ```
   Ask me anything: exit
   ```

## 🔄 Workflow

1. **Parallel Search Phase**: The system simultaneously queries Google, Bing, and Reddit
2. **Reddit Analysis Phase**: AI analyzes Reddit search results and selects the most relevant URLs
3. **Data Retrieval Phase**: Fetches detailed content from selected Reddit posts
4. **Individual Analysis Phase**: Each search source's results are analyzed separately by AI
5. **Synthesis Phase**: All analyses are combined into a comprehensive final answer

## 🎯 Use Cases

- **Research**: Gather diverse perspectives on any topic
- **Decision Making**: Compare information from different platforms
- **Market Research**: Understand public opinion through Reddit discussions
- **News Analysis**: Get multi-source coverage of current events

## 🔍 Example Output

The system provides structured analysis including:
- Google search insights (news, official sources, websites)
- Bing search results (alternative perspectives, different sources)
- Reddit community discussions (real user experiences, opinions)
- Synthesized recommendations combining all sources

## 🛠️ Configuration

The system uses a state-based architecture where each node processes specific data:

- `State`: TypedDict containing all workflow data
- `RedditURLAnalysis`: Pydantic model for structured Reddit URL selection
- `llm`: GPT-4 model for AI analysis and synthesis

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |
| `Bright_dataA_PI_KEY` | SERP API key for search operations | Yes |
| `REDDIT_CLIENT_ID` | Reddit API client ID | Yes |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | Yes |
| `REDDIT_USER_AGENT` | Reddit API user agent | Yes |



## 🔧 Troubleshooting

- **API Rate Limits**: Implement delays between requests if hitting rate limits
- **Missing Results**: Check API credentials and network connectivity
- **Empty Responses**: Verify search queries are properly formatted
- **Reddit Access**: Ensure Reddit API credentials are valid and have proper permissions

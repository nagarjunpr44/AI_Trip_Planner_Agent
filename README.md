# AI Agent Trip Planner

A sophisticated AI-powered trip planning system that intelligently extracts travel parameters from user queries and leverages multiple search engines to provide comprehensive travel recommendations. The system analyzes travel-related content from Google, Bing, and Reddit to create personalized trip plans and travel insights.

## 🌟 Features

- **Smart Trip Parameter Extraction**: Uses GPT-4 to automatically extract destination, duration, budget, and interests from natural language queries
- **Multi-Source Travel Research**: Simultaneously searches Google, Bing, and Reddit for comprehensive travel information gathering
- **AI-Powered Travel Analysis**: Uses GPT-4 to analyze search results and provide travel-specific insights
- **Reddit Travel Communities**: Intelligently selects relevant Reddit travel discussions and retrieves detailed community experiences
- **Parallel Processing**: Executes multiple search operations concurrently for faster trip planning
- **Travel-Focused Synthesis**: Combines analyses from all sources into comprehensive travel recommendations
- **Dual Interface**: Both command-line and web-based interfaces for trip planning queries

## 🏗️ Architecture

The system is built using LangGraph and follows a state-based workflow:

```
START
    ↓
Extract Trip Parameters (destination, days, budget, interests)
    ↓
┌── Google Search ──┐
├── Bing Search ────┤ (Parallel Execution)
└── Reddit Search ──┘
    ↓
Reddit URL Analysis & Selection
    ↓
Reddit Post & Comments Retrieval
    ↓
┌── Google Travel Analysis ──┐
├── Bing Travel Analysis ────┤ (Parallel Execution)
└── Reddit Community Analysis┘
    ↓
Travel Recommendations Synthesis
    ↓
END
```

## 🔧 Components

### Core Modules
- **backend/nodes/graph.py**: LangGraph workflow definition and node orchestration
- **backend/nodes/node_functions.py**: Core trip planning and search functions
- **backend/agent/prompts.py**: Travel-specific AI prompt templates
- **backend/agent/llm_wrapper.py**: GPT-4 integration and structured output handling
- **backend/data_sources/web_operations.py**: Search API integrations (Google, Bing, Reddit)
- **main.py**: Command-line interface for trip planning
- **backend/app.py**: FastAPI web service for trip planning API

### Key Functions
- `extract_trip_parameters()`: Extracts structured trip data (destination, days, budget, interests)
- `google_search()` / `bing_search()`: Perform travel-focused web searches using SERP API
- `reddit_search()`: Search Reddit for travel discussions and experiences
- `analyze_reddit_posts()`: AI-powered selection of valuable travel forum URLs
- `retrieve_reddit_posts()`: Extract detailed travel posts and community comments
- `analyze_*_results()`: Travel-specific analysis for each search source
- `synthesize_analyses()`: Combine all analyses into comprehensive trip recommendations

## 📋 Prerequisites

- Python 3.10+
- OpenAI API key (for GPT-4)
- SERP API key (for Google/Bing searches via Bright Data)
- Reddit API credentials (for community insights)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nagarjunpr44/AI_Agent_Trip_Planner.git
   cd AI_Agent_Trip_Planner
   ```

2. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
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
fastapi
uvicorn
```

## 💻 Usage

### Command Line Interface
1. **Start the trip planner**
   ```bash
   python main.py
   ```

2. **Plan your trip with natural language**
   ```
   Ask me anything: Plan a 7-day trip to Tokyo for $3000, interested in food and culture
   Ask me anything: I want to visit Paris for 5 days, love museums and cafes
   Ask me anything: Budget trip to Thailand for 10 days, into adventure activities
   ```

3. **Exit the application**
   ```
   Ask me anything: exit
   ```

### Web API Interface
1. **Start the FastAPI server**
   ```bash
   cd backend
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

2. **Access the API**
   - API endpoint: `POST http://localhost:8000/ask`
   - Web interface: Open `frontend/static/templates/index.html` in browser
   - API documentation: `http://localhost:8000/docs`

## 🔄 Workflow

1. **Trip Parameter Extraction**: AI extracts destination, duration, budget, and interests from user input
2. **Parallel Search Phase**: System simultaneously queries Google, Bing, and Reddit for travel information
3. **Reddit Analysis Phase**: AI analyzes Reddit travel results and selects most relevant community discussions
4. **Data Retrieval Phase**: Fetches detailed content from selected Reddit travel posts and comments
5. **Individual Analysis Phase**: Each search source's results are analyzed separately for travel insights
6. **Synthesis Phase**: All analyses are combined into comprehensive travel recommendations

## 🎯 Use Cases

- **Vacation Planning**: "Plan a 2-week honeymoon in Italy with a $5000 budget"
- **Business Travel Optimization**: "3-day business trip to Singapore, need good hotels near financial district"
- **Adventure Travel**: "Backpacking through Southeast Asia for a month, budget-friendly"
- **Cultural Exploration**: "Family trip to Japan for 10 days, interested in traditional culture and food"
- **City Breaks**: "Weekend getaway to Barcelona, love art and nightlife"

## 🔍 Example Output

The system provides structured travel recommendations including:

**Trip Parameters Extracted:**
- Destination: Tokyo, Japan
- Duration: 7 days
- Budget: $3000
- Interests: Food, Culture

**Multi-Source Analysis:**
- **Google Results**: Official tourism sites, hotel bookings, flight information
- **Bing Results**: Alternative travel perspectives, Microsoft travel services
- **Reddit Community**: Real traveler experiences, hidden gems, budget tips, cultural insights

**Final Recommendations:**
- Day-by-day itinerary suggestions
- Restaurant and food experience recommendations
- Cultural sites and activities
- Budget breakdown and money-saving tips
- Transportation options
- Community-recommended hidden spots

## 🛠️ Configuration

The system uses a state-based architecture with structured data models:

- `State`: TypedDict containing all trip planning workflow data
- `Triprequest`: Pydantic model for structured trip parameters (destination, days, budget, interests)
- `RedditURLAnalysis`: Pydantic model for structured Reddit URL selection
- `llm`: GPT-4 model for AI analysis and trip synthesis

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |
| `SERP_API_KEY` | SERP API key for Google/Bing searches | Yes |
| `REDDIT_CLIENT_ID` | Reddit API client ID for travel communities | Yes |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | Yes |
| `REDDIT_USER_AGENT` | Reddit API user agent string | Yes |

## 🌐 API Endpoints

### POST /ask
Submit a travel planning query and receive comprehensive recommendations.

**Request Body:**
```json
{
  "user_question": "Plan a 5-day trip to Paris for $2000, interested in art and food"
}
```

**Response:**
```json
{
  "final_answer": "Comprehensive travel plan with recommendations..."
}
```

## 🔧 Troubleshooting

- **API Rate Limits**: Implement delays between requests if hitting search API rate limits
- **Missing Travel Results**: Check API credentials and network connectivity
- **Empty Trip Plans**: Verify trip queries contain sufficient detail (destination, duration, interests)
- **Reddit Access Issues**: Ensure Reddit API credentials are valid and have proper permissions for travel subreddits
- **Trip Parameter Extraction**: If parameters aren't extracted correctly, try more specific language in queries

## 🚀 Future Enhancements

- Integration with booking APIs for direct reservations
- Real-time price monitoring and alerts
- Photo-based destination recommendations
- Multi-language support for international travelers
- Collaborative trip planning for groups

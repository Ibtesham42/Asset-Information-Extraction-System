# Asset Information Extraction System

An AI-powered system that extracts structured product information from web search using Large Language Models (LLM). Built for the Redpluto Analytics AI/ML assessment.

##  Overview


This system takes a product's model number and asset classification, performs intelligent web search, and returns validated JSON output with manufacturer, product line, and technical specifications.

##  Features

- **Intelligent Web Search**: Automatically builds optimized search queries
- **Multi-LLM Support**: Google Gemini & OpenAI GPT integration
- **Real-time Extraction**: Live data from Google search via Serper.dev
- **Robust Error Handling**: Automatic retries with exponential backoff
- **Fallback Mechanism**: Graceful degradation when extraction fails
- **RESTful API**: FastAPI with automatic Swagger documentation
- **Comprehensive Logging**: Debug and monitoring ready

##  Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python 3.10) |
| AI/LLM | Google Gemini / OpenAI GPT |
| Search API | Serper.dev (Google Search) |
| Validation | Pydantic |
| Container | Docker & Docker Compose |
| Testing | Pytest |

##  Prerequisites

- Python 3.10 or higher
- API Keys (free tiers available):
  - [Serper.dev](https://serper.dev) - 2,500 free searches
  - [Google Gemini](https://makersuite.google.com/app/apikey) - Free tier
  - OR [OpenAI](https://platform.openai.com/api-keys)

##  Installation

### 1. Clone Repository

git clone https://github.com/Ibtesham42/Asset-Information-Extraction-System.git

cd Asset-Information-Extraction-System/asset-info-extractor

## 2. Set Up Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies

pip install -r requirements.txt

# 4. Configure Environment Variables
    
    Create .env file:
    # API Keys


OPENAI_API_KEY="OPEN_AI_API_KEY"

SERPER_API_KEY="Serper_API_KEY"

# Model Configuration
DEFAULT_LLM_MODEL='openai/gpt-oss-20b'
MAX_RETRIES=5
RETRY_DELAY_SECONDS=2

# Search Configuration
MAX_SEARCH_RESULTS=5
SEARCH_TIMEOUT_SECONDS=10

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false


# 5. Run Application

    python -m src.main

# 6. Access API

Swagger Documentation: http://localhost:8000/docs

Health Check: http://localhost:8000/health

API Endpoint: http://localhost:8000/api/v1/extract


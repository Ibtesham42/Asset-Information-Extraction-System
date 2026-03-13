# Asset Information Extraction System Architecture

## Overview
This system extracts structured product information from web searches using AI/LLM technology.

## Components

### 1. API Layer (FastAPI)
- Handles HTTP requests/responses
- Input validation using Pydantic models
- Swagger documentation at `/docs`

### 2. Search Service
- Builds optimized search queries
- Interfaces with Google Search API/SerpAPI
- Returns relevant search results

### 3. LLM Service
- Supports Gemini and GPT models
- Extracts structured data from search results
- Returns JSON-formatted information

### 4. Extraction Service (Orchestrator)
- Coordinates the entire process
- Implements retry logic
- Handles fallback scenarios

### 5. Utils
- Logging with rotation
- Retry decorators
- Data validation

## Data Flow
1. Client sends POST request with asset information
2. System validates input
3. Search service performs web search
4. LLM extracts structured data
5. Response is validated and returned

## Error Handling
- Automatic retries (up to 5 times)
- Fallback responses when extraction fails
- Comprehensive logging

## Deployment
- Environment-based configuration
- Health checks for monitoring

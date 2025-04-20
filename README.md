
# AI Model Playground

A web application for comparing responses from different AI models side-by-side with detailed performance metrics.

## Project Structure and Architecture

### Backend
- **Framework**: FastAPI
- **Key Components**:
  - API endpoints (handlers/)
  - Services for AI providers (services/)
  - Database models (models/)
  - Repositories (repositories/)

### Frontend
- **Framework**: React with TypeScript
- **UI Library**: Chakra UI
- **State Management**: Zustand
- **Key Features**:
  - Side-by-side model comparison
  - Response history tracking

### Data Flow
1. Frontend → FastAPI → AI Providers
2. Response Processing → Frontend

## Setup Instructions

### Backend
1. Install Python 3.9+
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` using `.env.example`
6. Run: `uvicorn app:app --reload`

### Frontend
1. Install Node.js 16+
2. Install dependencies: `npm install`
3. Run: `npm run dev`

## Technical Decisions & Tradeoffs

1. **FastAPI Choice**:
   - Pros: Async support, automatic docs, Python ecosystem
   - Cons: Less mature than Django for complex apps

2. **React + Zustand**:
   - Pros: Lightweight state management, better performance than Redux
   - Cons: Less opinionated than Redux Toolkit

3. **Scroll Sync**:
   - Implemented via DOM manipulation for simplicity
   - Alternative: Could use a shared scroll context

## Future Improvements

1. **Enhanced Comparison**:
   - Add more metrics (accuracy, relevance scoring)
   - Support for image generation models

2. **Performance**:
   - Implement response streaming
   - Add client-side caching

3. **Features**:
   - User authentication
   - Team collaboration features
   - Custom model configurations
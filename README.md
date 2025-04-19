# AI Model Playground

A web application for comparing responses from different AI models side-by-side.

## Backend Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables (see `.env.example`)
3. Run the development server: `python app.py`

## Project Structure

```
ai-model-playground/
├── app.py                # Main application entry point
├── requirements.txt      # Python dependencies
├── .env.example          # Environment configuration template
├── services/             # AI provider integration services
├── models/               # Database models
├── utils/                # Utility functions (token counting, etc.)
└── api/                  # API routes
```
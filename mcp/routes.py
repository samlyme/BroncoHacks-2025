import os
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import uvicorn
from datetime import datetime, timedelta
import pandas as pd

# Import the SimpleMCPClient from main.py
from main import SimpleMCPClient

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="MCP API",
    description="API for Claude MCP (Message/Context Processing) system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Get configuration from environment variables
api_key = os.environ.get("ANTHROPIC_API_KEY") or "your_api_key_here"
db_url = os.environ.get(
    "DATABASE_URL") or "postgresql://username:password@localhost:5432/database_name"

# Initialize MCP client
client = SimpleMCPClient(api_key, db_url)

# Define request and response models


class FetchQuestionsParams(BaseModel):
    limit: int = 1000
    days_back: Optional[int] = None


class CommonQuestion(BaseModel):
    title: str
    examples: List[str]
    explanation: str


class AnalysisRequest(BaseModel):
    limit: int = 1000
    days_back: Optional[int] = None
    output_dir: str = "study_guides"

# Endpoints


@app.get("/")
async def root():
    return {"message": "Welcome to the MCP API"}


@app.get("/health")
async def health_check():
    try:
        # Just test that we can access the engine
        engine = client.engine
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/fetch-questions")
async def fetch_questions(params: FetchQuestionsParams):
    try:
        df = client.fetch_user_questions(
            limit=params.limit, days_back=params.days_back)
        if len(df) == 0:
            return {"warning": "No messages found", "messages": []}

        # Convert DataFrame to list of dicts for JSON response
        messages = df.to_dict(orient="records")

        # Format datetime objects for JSON serialization
        for msg in messages:
            if "created_at" in msg and isinstance(msg["created_at"], datetime):
                msg["created_at"] = msg["created_at"].isoformat()

        return {"message_count": len(messages), "messages": messages}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching questions: {str(e)}")


@app.post("/identify-common-questions")
async def identify_common_questions(params: FetchQuestionsParams):
    try:
        # First fetch the messages
        df = client.fetch_user_questions(
            limit=params.limit, days_back=params.days_back)
        if len(df) == 0:
            return {"warning": "No messages found", "common_questions": []}

        # Then identify common questions
        analysis_results = client.identify_common_questions(df)
        return analysis_results
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error identifying common questions: {str(e)}")


@app.post("/generate-study-guide")
async def generate_study_guide(question: CommonQuestion):
    try:
        # Generate a single study guide
        study_guides = client.generate_study_guides([question.dict()])
        return {"title": question.title, "study_guide": study_guides.get(question.title, "")}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating study guide: {str(e)}")


@app.post("/save-study-guides")
async def save_study_guides(
    study_guides: Dict[str, str],
    output_dir: str = Query(
        "study_guides", description="Directory to save study guides in")
):
    try:
        file_paths = client.save_study_guides(study_guides, output_dir)
        return {"file_paths": file_paths}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving study guides: {str(e)}")


@app.post("/create-index")
async def create_index(
    study_guides: Dict[str, str],
    file_paths: Dict[str, str],
    output_dir: str = Query(
        "study_guides", description="Directory to save index in")
):
    try:
        index_path = client.create_index_page(
            study_guides, file_paths, output_dir)
        return {"index_path": index_path}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating index: {str(e)}")


@app.post("/run-full-pipeline")
async def run_full_pipeline(params: AnalysisRequest):
    try:
        results = client.run(
            limit=params.limit, days_back=params.days_back, output_dir=params.output_dir)

        # Check for errors
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])

        # Format any datetime objects for JSON serialization
        if "common_questions" in results:
            for question in results["common_questions"]:
                if "created_at" in question and isinstance(question["created_at"], datetime):
                    question["created_at"] = question["created_at"].isoformat()

        return results
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error running pipeline: {str(e)}")

# Main entry point
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=7070, reload=True)

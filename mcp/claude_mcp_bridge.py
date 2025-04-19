from fastapi import FastAPI, HTTPException, Body
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import uvicorn
import requests
import threading
import json
from collections import Counter
import re
from anthropic import Anthropic

load_dotenv()

class Question(BaseModel):
    content: str

class TopicRequest(BaseModel):
    limit: int = 100
    min_questions: int = 3

class StudyGuideRequest(BaseModel):
    topic: str
    examples: List[str]
    output_file: Optional[str] = None

class ClaudeMCPBridge:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.app = FastAPI(title="MCP Server")
        self.setup_routes()
        
        # Database setup
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("No DATABASE_URL found in environment variables")
        self.engine = create_engine(self.database_url)
        
        # Anthropic API setup
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("No ANTHROPIC_API_KEY found in environment variables")
        self.claude_client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-7-sonnet-20250219"  # Use the latest model

    def setup_routes(self):
        """Set up FastAPI routes"""
        
        @self.app.get("/api/user-questions", response_model=List[Question])
        async def get_user_questions():
            try:
                query = text("""
                    SELECT content
                    FROM message
                    WHERE 
                        role = 'user'
                        AND content LIKE '%?%'
                    ORDER BY created_at DESC
                """)
                
                with self.engine.connect() as connection:
                    result = connection.execute(query)
                    questions = [Question(content=row.content) for row in result]
                    return questions
                    
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy"}
            
        @self.app.post("/api/summarize-topics")
        async def summarize_topics(request: TopicRequest = Body(...)):
            try:
                # Fetch questions
                query = text(f"""
                    SELECT content
                    FROM message
                    WHERE 
                        role = 'user'
                        AND content LIKE '%?%'
                    ORDER BY created_at DESC
                    LIMIT {request.limit}
                """)
                
                with self.engine.connect() as connection:
                    result = connection.execute(query)
                    questions = [row.content for row in result]
                
                if not questions:
                    return {"error": "No questions found in the database"}
                
                # Call topic identification function
                topics = self.identify_question_topics(questions, request.min_questions)
                return topics
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error summarizing topics: {str(e)}")
                
        @self.app.post("/api/generate-study-guide")
        async def generate_study_guide(request: StudyGuideRequest):
            try:
                study_guide = self.generate_study_guide(
                    topic=request.topic, 
                    examples=request.examples,
                    output_file=request.output_file
                )
                return {"study_guide": study_guide}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error generating study guide: {str(e)}")

    def start_server(self):
        """Start the FastAPI server in a separate thread"""
        def run_server():
            uvicorn.run(self.app, host="0.0.0.0", port=3000)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

    def fetch_user_questions(self) -> List[Dict[str, Any]]:
        """Fetch user questions from the MCP server"""
        try:
            response = requests.get(f"{self.base_url}/api/user-questions")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch questions: {str(e)}")

    def calculate_statistics(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics about the questions"""
        total_questions = len(questions)
        
        if total_questions == 0:
            return {
                "total_questions": 0,
                "average_length": 0,
                "length_distribution": {
                    "Short (< 50 chars)": 0,
                    "Medium (50-150 chars)": 0,
                    "Long (> 150 chars)": 0
                }
            }

        # Calculate average length
        avg_length = sum(len(q['content']) for q in questions) / total_questions

        # Calculate length distribution
        length_ranges = {
            "Short (< 50 chars)": 0,
            "Medium (50-150 chars)": 0,
            "Long (> 150 chars)": 0
        }

        for q in questions:
            length = len(q['content'])
            if length < 50:
                length_ranges["Short (< 50 chars)"] += 1
            elif length <= 150:
                length_ranges["Medium (50-150 chars)"] += 1
            else:
                length_ranges["Long (> 150 chars)"] += 1

        return {
            "total_questions": total_questions,
            "average_length": avg_length,
            "length_distribution": length_ranges
        }

    def health_check(self) -> bool:
        """Check if the MCP server is running"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except requests.RequestException:
            return False
            
    def identify_question_topics(self, questions: List[str], min_questions: int = 3) -> Dict[str, Any]:
        """
        Use Claude to identify common topics in user questions
        
        Args:
            questions: List of question strings
            min_questions: Minimum number of questions for a topic to be included
            
        Returns:
            Dictionary with topic analysis results
        """
        # Create a sample if there are too many questions
        if len(questions) > 100:
            import random
            random.seed(42)  # For reproducibility
            questions_sample = random.sample(questions, 100)
        else:
            questions_sample = questions
            
        # Create prompt for Claude
        prompt = f"""
        I have a dataset of {len(questions)} user questions from Claude desktop conversations.
        Here's a sample of {len(questions_sample)} questions:
        
        {json.dumps(questions_sample, indent=2)}
        
        Please identify the 5-10 most common question topics that users are asking about.
        Only include topics that appear in at least {min_questions} different questions.
        
        For each common topic:
        1. Provide a clear title for the topic
        2. List 2-3 example questions that represent this topic
        3. Explain why users might be asking about this topic
        
        Format the response as JSON with the following structure:
        {{
            "common_topics": [
                {{
                    "title": "topic title",
                    "examples": ["example question 1", "example question 2"],
                    "explanation": "why users ask about this topic"
                }}
            ]
        }}
        """
        
        # Call Claude API
        try:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract and parse the JSON response
            response_text = response.content[0].text
            json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response_text
                
            analysis_results = json.loads(json_str)
            return analysis_results
            
        except Exception as e:
            print(f"Error identifying topics: {e}")
            return {"error": f"Failed to identify topics: {str(e)}"}
    
    def generate_study_guide(self, topic: str, examples: List[str], output_file: Optional[str] = None) -> str:
        """
        Generate a comprehensive study guide for a specific question topic
        
        Args:
            topic: Title of the topic
            examples: Example questions for this topic
            output_file: Optional file path to save the guide
            
        Returns:
            The generated study guide as a string
        """
        # Create prompt for Claude
        prompt = f"""
        I need to create a comprehensive study guide for this common user question/topic:
        
        TOPIC: {topic}
        
        Example questions from users:
        {json.dumps(examples, indent=2)}
        
        Please create a detailed study guide that:
        1. Clearly explains the topic/answers the question
        2. Provides step-by-step instructions where applicable
        3. Includes examples or scenarios to illustrate key points
        4. Anticipates follow-up questions and addresses them
        5. Uses a friendly, easy-to-understand tone suitable for all user levels
        
        Format the study guide in Markdown with appropriate headings, bullet points, code blocks, etc.
        """
        
        # Call Claude API
        try:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Get the study guide content
            study_guide = response.content[0].text
            
            # Save to file if requested
            if output_file:
                os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(study_guide)
                    
            return study_guide
            
        except Exception as e:
            print(f"Error generating study guide: {e}")
            return f"Failed to generate study guide: {str(e)}"

# If running this file directly, start the server
if __name__ == "__main__":
    bridge = ClaudeMCPBridge()
    bridge.start_server()
    # Keep the main thread alive
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
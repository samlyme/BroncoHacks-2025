import os
import json
from dotenv import load_dotenv
import pandas as pd
import re
from anthropic import Anthropic
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select, create_engine
from models import Message


class SimpleMCPClient:
    """
    Simplified MCP client that identifies common user questions
    and generates study guides to answer them.
    """

    def __init__(self, api_key: str, db_url: str):
        """
        Initialize the MCP client with API key and database connection.

        Args:
            api_key: Anthropic API key for Claude
            db_url: SQLAlchemy database URL for PostgreSQL connection
        """
        self.api_key = api_key
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-7-sonnet-20250219"
        print("MCP client initialized")

    def fetch_user_questions(self, limit: int = 1000, days_back: Optional[int] = None) -> pd.DataFrame:
        """
        Fetch user messages from the database.

        Args:
            limit: Maximum number of messages to retrieve
            days_back: Optional number of days to look back

        Returns:
            DataFrame containing user messages
        """
        try:
            with Session(self.engine) as session:
                # Start with base query
                query = select(
                    Message.message_id,
                    Message.content,
                    Message.user_id,
                    Message.created_at
                )

                # Filter to only user messages (not assistant messages)
                query = query.where(Message.role == "user")

                # Add time filter if specified
                if days_back:
                    cutoff_date = datetime.utcnow() - timedelta(days=days_back)
                    query = query.where(Message.created_at >= cutoff_date)

                # Order and limit
                query = query.order_by(Message.created_at.desc()).limit(limit)

                # Execute query
                results = session.exec(query).all()

                # Convert to DataFrame
                records = []
                for msg in results:
                    records.append({
                        "message_id": msg.message_id,
                        "content": msg.content,
                        "user_id": msg.user_id,
                        "created_at": msg.created_at
                    })

                df = pd.DataFrame(records)
                print(f"Retrieved {len(df)} messages from database")
                return df

        except Exception as e:
            print(f"Error fetching messages: {e}")
            return pd.DataFrame()

    def identify_common_questions(self, messages: pd.DataFrame) -> Dict[str, Any]:
        """
        Use Claude to identify the most common questions from user messages.

        Args:
            messages: DataFrame containing user messages

        Returns:
            Dictionary with common questions analysis
        """
        # Prepare a sample of messages for Claude to analyze
        message_sample = messages['content'].tolist()

        # If there are too many messages, sample them
        if len(message_sample) > 100:
            import random
            random.seed(42)  # For reproducibility
            message_sample = random.sample(message_sample, 100)

        # Create the prompt for Claude
        prompt = f"""
        I have a dataset of {len(messages)} user messages. Here's a sample of {len(message_sample)} messages:
        
        {json.dumps(message_sample, indent=2)}
        
        Please identify the 5-10 most common questions or topics that users are asking about.
        For each common question/topic:
        1. Provide a clear title for the question/topic
        2. List 2-3 example messages that represent this question/topic
        3. Explain why users might be asking this question
        
        Format the response as JSON with the following structure:
        {{
            "common_questions": [
                {{
                    "title": "question/topic title",
                    "examples": ["example message 1", "example message 2"],
                    "explanation": "why users ask this"
                }}
            ]
        }}
        """

        # Call Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and parse the JSON response
        try:
            response_text = response.content[0].text
            json_match = re.search(
                r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response_text

            analysis_results = json.loads(json_str)
            return analysis_results

        except json.JSONDecodeError as e:
            print(f"Error parsing Claude's response: {e}")
            print(f"Raw response: {response_text}")
            return {"error": "Failed to parse Claude's response", "raw_response": response_text}

    def generate_study_guides(self, common_questions: List[Dict]) -> Dict[str, str]:
        """
        Generate study guides for each common question identified.

        Args:
            common_questions: List of common question dictionaries

        Returns:
            Dictionary mapping question titles to study guides
        """
        study_guides = {}

        for question in common_questions:
            title = question["title"]
            examples = question["examples"]
            explanation = question.get("explanation", "")

            print(f"Generating study guide for: {title}")

            # Create the prompt for Claude
            prompt = f"""
            I need to create a comprehensive study guide for this common user question/topic:
            
            TOPIC: {title}
            
            Example questions from users:
            {json.dumps(examples, indent=2)}
            
            Context on why users ask this: {explanation}
            
            Please create a detailed study guide that:
            1. Clearly explains the topic/answers the question
            2. Provides step-by-step instructions where applicable
            3. Includes examples or scenarios to illustrate key points
            4. Anticipates follow-up questions and addresses them
            5. Uses a friendly, easy-to-understand tone suitable for all user levels
            
            Format the study guide in Markdown with appropriate headings, bullet points, code blocks, etc.
            """

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Store the study guide
            study_guides[title] = response.content[0].text

        return study_guides

    def save_study_guides(self, study_guides: Dict[str, str], output_dir: str = "study_guides") -> Dict[str, str]:
        """
        Save generated study guides to files.

        Args:
            study_guides: Dictionary mapping question titles to study guides
            output_dir: Directory to save study guides in

        Returns:
            Dictionary mapping question titles to file paths
        """
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save each study guide to a file
        file_paths = {}
        for title, content in study_guides.items():
            # Create a filename from the title
            filename = title.lower().replace(" ", "_").replace("/", "_").replace("?", "")
            filename = re.sub(r'[^\w\s-]', '', filename)
            filename = f"{filename}.md"
            file_path = os.path.join(output_dir, filename)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            file_paths[title] = file_path
            print(f"Saved study guide for '{title}' to {file_path}")

        return file_paths

    def create_index_page(self, study_guides: Dict[str, str], file_paths: Dict[str, str], output_dir: str = "study_guides") -> str:
        """
        Create an index page that links to all study guides.

        Args:
            study_guides: Dictionary mapping question titles to study guides
            file_paths: Dictionary mapping question titles to file paths
            output_dir: Directory to save index page in

        Returns:
            Path to the index file
        """
        index_path = os.path.join(output_dir, "index.md")

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# Common Questions Study Guides\n\n")
            f.write(
                f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for title, file_path in file_paths.items():
                relative_path = os.path.basename(file_path)
                f.write(f"- [{title}]({relative_path})\n")

        print(f"Created index page at {index_path}")
        return index_path

    def run(self, limit: int = 1000, days_back: Optional[int] = None, output_dir: str = "study_guides") -> Dict[str, Any]:
        """
        Run the complete pipeline: fetch questions, identify common ones, and generate study guides.

        Args:
            limit: Maximum number of messages to analyze
            days_back: Optional number of days to look back
            output_dir: Directory to save study guides in

        Returns:
            Dictionary with results
        """
        # Step 1: Fetch user messages
        print("Fetching user messages...")
        messages_df = self.fetch_user_questions(limit, days_back)
        if len(messages_df) == 0:
            return {"error": "No messages found in the database"}

        # Step 2: Identify common questions
        print("Identifying common questions...")
        analysis_results = self.identify_common_questions(messages_df)

        common_questions = analysis_results.get("common_questions", [])
        if not common_questions:
            return {"error": "No common questions identified", "raw_analysis": analysis_results}

        # Step 3: Generate study guides for each common question
        print(
            f"Generating study guides for {len(common_questions)} common questions...")
        study_guides = self.generate_study_guides(common_questions)

        # Step 4: Save study guides to files
        print("Saving study guides...")
        file_paths = self.save_study_guides(study_guides, output_dir)

        # Step 5: Create an index page
        print("Creating index page...")
        index_path = self.create_index_page(
            study_guides, file_paths, output_dir)

        # Return results
        return {
            "common_questions": common_questions,
            "study_guides": study_guides,
            "file_paths": file_paths,
            "index_path": index_path
        }


load_dotenv()
# Example usage
if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY") or "your_api_key_here"
    db_url = os.environ.get(
        "DATABASE_URL") or "postgresql://username:password@localhost:5432/database_name"

    client = SimpleMCPClient(api_key, db_url)
    results = client.run(limit=500, days_back=30)

    print("\nProcess complete!")
    if "index_path" in results:
        print(f"Study guides index available at: {results['index_path']}")

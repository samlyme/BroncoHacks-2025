import requests
import json
import sys


def call_mcp_api(endpoint, data=None):
    """
    Call the MCP API with the specified endpoint and data
    """
    base_url = "http://localhost:7070"
    url = f"{base_url}/{endpoint}"

    try:
        if data:
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)

        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return {"error": str(e)}


def check_health():
    """Check if the MCP API is running"""
    return call_mcp_api("health")


def run_analysis(limit=500, days_back=30):
    """Run the full analysis pipeline"""
    data = {
        "limit": limit,
        "days_back": days_back,
        "output_dir": "study_guides"
    }
    return call_mcp_api("run-full-pipeline", data)


def fetch_common_questions(limit=500, days_back=30):
    """Fetch and identify common questions"""
    data = {
        "limit": limit,
        "days_back": days_back
    }
    return call_mcp_api("identify-common-questions", data)

# Main function with simple command line interface


def main():
    if len(sys.argv) < 2:
        print("Usage: python claude_mcp_bridge.py [health|analyze|questions]")
        return

    command = sys.argv[1].lower()

    if command == "health":
        result = check_health()
    elif command == "analyze":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 500
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        result = run_analysis(limit, days)
    elif command == "questions":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 500
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        result = fetch_common_questions(limit, days)
    else:
        result = {"error": f"Unknown command: {command}"}

    # Pretty print the result
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

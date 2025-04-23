"""Entry point script for SuperNova AI."""

import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.workflow import run_agent_workflow

# Load environment variables
load_dotenv()

def test_connection():
    """Test the connection to Ollama."""
    print("Testing connection to Ollama...")

    # Get model configuration from environment
    reasoning_model = os.getenv("REASONING_MODEL", "llama3.2")
    reasoning_base_url = os.getenv("REASONING_BASE_URL", "http://localhost:11434/v1")

    print(f"Using model: {reasoning_model}")
    print(f"Base URL: {reasoning_base_url}")

    try:
        # Initialize the LLM
        llm = ChatOpenAI(
            model=reasoning_model,
            base_url=reasoning_base_url,
            api_key="not-needed-for-ollama",
            temperature=0.7,
        )

        # Test the LLM with a simple query
        response = llm.invoke("Hello! Can you tell me about yourself and confirm you're running locally via Ollama?")

        print("\nResponse from LLM:")
        print("-" * 40)
        print(response.content)
        print("-" * 40)
        print("Connection test successful!\n")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main entry point for the application."""
    print("Langmanus with Ollama")
    print("=" * 40)

    # Test connection to Ollama
    if not test_connection():
        print("Failed to connect to Ollama. Please make sure Ollama is running.")
        return 1

    # Get user query
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Enter your query: ")

    # Run the agent workflow
    print("\nProcessing your query...\n")
    result = run_agent_workflow(user_input=user_query, debug=True)

    # Print the conversation history
    print("\n=== Conversation History ===")
    for message in result["messages"]:
        role = message.type
        print(f"\n[{role.upper()}]: {message.content}")

    return 0

if __name__ == "__main__":
    sys.exit(main())

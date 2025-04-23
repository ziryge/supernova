import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

def main():
    """
    Main entry point for the application.
    Creates a simple chat interface with memory.
    """
    print("Langmanus Simple Chat with Ollama")
    print("-" * 40)
    
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
        
        # Create a conversation memory
        memory = ConversationBufferMemory(return_messages=True)
        
        # Create a prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant running locally via Ollama."),
            ("human", "{input}"),
            ("ai", "{history}"),
        ])
        
        # Create a conversation chain
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            verbose=True
        )
        
        # Run the conversation in a loop
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
                
            # Get the response
            response = conversation.predict(input=user_input)
            
            print(f"\nAI: {response}")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

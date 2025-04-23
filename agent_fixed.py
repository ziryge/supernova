import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Define some simple tools
@tool
def search_wikipedia(query: str) -> str:
    """Search for information about a topic on a simulated Wikipedia."""
    return f"Here is some information about {query}: This is simulated Wikipedia content for demonstration purposes."

@tool
def calculate(expression: str) -> str:
    """Calculate the result of a mathematical expression."""
    try:
        return f"The result of {expression} is {eval(expression)}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

@tool
def current_date() -> str:
    """Get the current date."""
    from datetime import datetime
    return f"The current date is {datetime.now().strftime('%Y-%m-%d')}"

def create_agent():
    """Create a Langmanus agent using Ollama."""
    # Get model configuration from environment
    reasoning_model = os.getenv("REASONING_MODEL", "llama3.2")
    reasoning_base_url = os.getenv("REASONING_BASE_URL", "http://localhost:11434/v1")
    
    print(f"Creating agent with model: {reasoning_model}")
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model=reasoning_model,
        base_url=reasoning_base_url,
        api_key="not-needed-for-ollama",
        temperature=0.7,
    )
    
    # Define tools
    tools = [search_wikipedia, calculate, current_date]
    
    # Create a prompt template with the agent_scratchpad
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant that can use tools to answer questions.
        Think step by step about what the user is asking, and use the appropriate tools when needed.
        If you don't know the answer or don't have the right tools, be honest about it."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def main():
    """Main function to run the agent."""
    print("Langmanus Agent with Ollama")
    print("-" * 40)
    
    try:
        # Create the agent
        agent = create_agent()
        
        # Run the agent in a loop
        while True:
            user_input = input("\nEnter your question (or 'exit' to quit): ")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
                
            # Process the user input
            response = agent.invoke({"input": user_input})
            
            print("\nAgent Response:")
            print("-" * 40)
            print(response["output"])
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()

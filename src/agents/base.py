"""
Base agent class for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint

from ..config.env import LLMConfig
from ..prompts.template import format_prompt

class BaseAgent:
    """Base agent class for all agents."""

    def __init__(self, agent_type: str, use_reasoning_llm: bool = True):
        """
        Initialize the base agent.

        Args:
            agent_type: Type of agent (supervisor, researcher, coder, etc.)
            use_reasoning_llm: Whether to use the reasoning LLM or basic LLM
        """
        self.agent_type = agent_type
        self.use_reasoning_llm = use_reasoning_llm
        self.messages = []

        # Load system prompt
        self.system_prompt = format_prompt(agent_type)
        self.messages.append(SystemMessage(content=self.system_prompt))

        # Check if we're running on Streamlit Cloud
        is_streamlit_cloud = os.environ.get('STREAMLIT_SHARING_MODE') == 'streamlit' or 'STREAMLIT_RUNTIME' in os.environ

        # Check for available API keys
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        groq_api_key = os.environ.get('GROQ_API_KEY')
        hf_api_key = os.environ.get('HUGGINGFACE_API_KEY')

        # If we're on Streamlit Cloud, try to use one of the cloud providers
        if is_streamlit_cloud:
            # First try Hugging Face with DeepSeek if available
            if hf_api_key:
                print("Running on Streamlit Cloud, using Hugging Face API with DeepSeek model")
                try:
                    if use_reasoning_llm:
                        # Use DeepSeek Coder model for reasoning
                        self.llm = HuggingFaceEndpoint(
                            repo_id="deepseek-ai/deepseek-coder-33b-instruct",
                            huggingfacehub_api_token=hf_api_key,
                            temperature=0.7,
                            max_length=4096,
                        )
                    else:
                        # Use DeepSeek model for basic tasks
                        self.llm = HuggingFaceEndpoint(
                            repo_id="deepseek-ai/deepseek-llm-7b-chat",
                            huggingfacehub_api_token=hf_api_key,
                            temperature=0.7,
                            max_length=2048,
                        )
                    # Set a flag to indicate we're using a regular LLM
                    self.using_chat_model = False
                except Exception as e:
                    print(f"Error initializing Hugging Face: {str(e)}")
                    # Fall back to Groq if available
                    if groq_api_key:
                        self._initialize_groq(use_reasoning_llm, groq_api_key)
                    # Or fall back to OpenAI if available
                    elif openai_api_key:
                        self._initialize_openai(use_reasoning_llm, openai_api_key)
                    else:
                        self._create_error_llm("Hugging Face initialization failed. Please check your API key.")
            # Try Groq if Hugging Face is not available
            elif groq_api_key:
                self._initialize_groq(use_reasoning_llm, groq_api_key)
            # Use OpenAI if neither Hugging Face nor Groq is available
            elif openai_api_key:
                self._initialize_openai(use_reasoning_llm, openai_api_key)
            else:
                # No API keys available
                print("No API keys available for cloud providers")
                self._create_error_llm("No API keys available. Please add HUGGINGFACE_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY to your secrets.")
        else:
            # Not on Streamlit Cloud, use Ollama for local development
            print("Using local Ollama")
            # Clean up model names for Ollama compatibility
            if use_reasoning_llm:
                # Use reasoning model (more capable)
                model_name = LLMConfig.REASONING_MODEL.replace(".2", "").replace(".1", "")  # Remove version suffix
                if ":" in model_name:  # Remove size suffix if present
                    model_name = model_name.split(":")[0]
            else:
                # Use basic model (faster)
                model_name = LLMConfig.BASIC_MODEL.replace(".2", "").replace(".1", "")  # Remove version suffix
                if ":" in model_name:  # Remove size suffix if present
                    model_name = model_name.split(":")[0]

            # Initialize Ollama LLM
            try:
                self.llm = Ollama(
                    model=model_name,
                    base_url="http://localhost:11434",
                    temperature=0.7,
                )
                # Set a flag to indicate we're using a regular LLM
                self.using_chat_model = False
            except Exception as e:
                # If Ollama initialization fails, print error and create a simple error-returning LLM
                print(f"Error initializing Ollama: {str(e)}")
                self._create_error_llm("I'm sorry, but I couldn't connect to Ollama. Please make sure Ollama is running.")

    def _initialize_groq(self, use_reasoning_llm: bool, api_key: str):
        """Initialize Groq LLM."""
        print("Running on Streamlit Cloud, using Groq API")
        try:
            if use_reasoning_llm:
                # Use a more capable model for reasoning
                self.llm = ChatGroq(
                    model="llama3-70b-8192",  # Llama 3 70B model
                    groq_api_key=api_key,
                    temperature=0.7,
                )
            else:
                # Use a faster model for basic tasks
                self.llm = ChatGroq(
                    model="llama3-8b-8192",  # Llama 3 8B model (faster)
                    groq_api_key=api_key,
                    temperature=0.7,
                )
            # Set a flag to indicate we're using a chat model
            self.using_chat_model = True
        except Exception as e:
            print(f"Error initializing Groq: {str(e)}")
            # Fall back to OpenAI if available
            openai_api_key = os.environ.get('OPENAI_API_KEY')
            if openai_api_key:
                self._initialize_openai(use_reasoning_llm, openai_api_key)
            else:
                self._create_error_llm("Groq initialization failed. Please check your API key.")

    def _initialize_openai(self, use_reasoning_llm: bool, api_key: str):
        """Initialize OpenAI LLM."""
        print("Running on Streamlit Cloud, using OpenAI API")
        try:
            if use_reasoning_llm:
                # Use a more capable model for reasoning
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",  # You can change this to gpt-4 if needed
                    openai_api_key=api_key,
                    temperature=0.7,
                )
            else:
                # Use a faster model for basic tasks
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    openai_api_key=api_key,
                    temperature=0.7,
                )
            # Set a flag to indicate we're using a chat model
            self.using_chat_model = True
        except Exception as e:
            print(f"Error initializing OpenAI: {str(e)}")
            self._create_error_llm("OpenAI initialization failed. Please check your API key.")

    def _create_error_llm(self, error_message: str):
        """Create a simple error-returning LLM."""
        from langchain.llms.base import LLM

        class ErrorLLM(LLM):
            message: str = error_message

            def _call(self, prompt: str, **kwargs) -> str:
                return self.message

            @property
            def _identifying_params(self) -> Dict[str, Any]:
                return {"message": self.message}

            @property
            def _llm_type(self) -> str:
                return "error"

        # Initialize the error LLM
        self.llm = ErrorLLM(message=error_message)
        self.using_chat_model = False

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.

        Args:
            role: Role of the message sender (human or ai)
            content: Content of the message
        """
        if role.lower() == "human":
            self.messages.append(HumanMessage(content=content))
        elif role.lower() == "ai":
            self.messages.append(AIMessage(content=content))

    def get_response(self, query: str) -> str:
        """
        Get a response from the agent.

        Args:
            query: Query to send to the agent

        Returns:
            Response from the agent
        """
        # Add the query to the conversation history
        self.add_message("human", query)

        try:
            # Handle different LLM types
            if hasattr(self, 'using_chat_model') and self.using_chat_model:
                # For chat models like OpenAI
                response = self.llm.invoke(self.messages)
                response_text = response.content if hasattr(response, 'content') else str(response)
            else:
                # For regular LLMs like Ollama
                prompt = self._messages_to_prompt(self.messages)
                response_text = self.llm(prompt)

            # Add the response to the conversation history
            self.add_message("ai", response_text)

            return response_text
        except Exception as e:
            # Handle errors gracefully
            error_message = f"Error getting response: {str(e)}"
            print(error_message)

            # Add a fallback response to the conversation history
            fallback_response = "I'm sorry, but I encountered an error while processing your request. Please try again."
            self.add_message("ai", fallback_response)

            return fallback_response

    def _messages_to_prompt(self, messages) -> str:
        """
        Convert a list of messages to a prompt string for regular LLMs.

        Args:
            messages: List of messages

        Returns:
            Prompt string
        """
        prompt_parts = []

        for message in messages:
            if isinstance(message, SystemMessage):
                prompt_parts.append(f"System: {message.content}\n")
            elif isinstance(message, HumanMessage):
                prompt_parts.append(f"Human: {message.content}\n")
            elif isinstance(message, AIMessage):
                prompt_parts.append(f"AI: {message.content}\n")
            else:
                prompt_parts.append(f"{message.type}: {message.content}\n")

        return "\n".join(prompt_parts)

    def reset(self) -> None:
        """Reset the agent's conversation history."""
        self.messages = [SystemMessage(content=self.system_prompt)]

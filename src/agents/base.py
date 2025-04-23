"""
Base agent class for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Import the fallback LLM configuration
from ..config.env import LLMConfig
from ..prompts.template import format_prompt

# Import the LLM fallback module
try:
    from ..config.llm_fallback import create_llm, is_ollama_available
    FALLBACK_AVAILABLE = True
except ImportError:
    FALLBACK_AVAILABLE = False

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

        # Initialize the LLM with fallback support
        if FALLBACK_AVAILABLE:
            # Check if we're running on Streamlit Cloud
            is_streamlit_cloud = os.environ.get('STREAMLIT_SHARING_MODE') == 'streamlit' or 'STREAMLIT_RUNTIME' in os.environ

            # Use the fallback LLM configuration
            if is_streamlit_cloud or not is_ollama_available():
                # Use the fallback LLM
                self.llm = create_llm()
            else:
                # Use Ollama
                if use_reasoning_llm:
                    from langchain_community.llms import Ollama
                    self.llm = Ollama(
                        model=LLMConfig.REASONING_MODEL.replace(".2", "").replace(".1", ""),  # Remove version suffix
                        base_url="http://localhost:11434",
                        temperature=0.7,
                    )
                else:
                    from langchain_community.llms import Ollama
                    self.llm = Ollama(
                        model=LLMConfig.BASIC_MODEL.replace(".2", "").replace(".1", "").split(":")[0],  # Remove version suffix and size
                        base_url="http://localhost:11434",
                        temperature=0.7,
                    )
        else:
            # Fallback not available, use standard configuration
            try:
                # Try to use Ollama
                from langchain_community.llms import Ollama
                if use_reasoning_llm:
                    self.llm = Ollama(
                        model=LLMConfig.REASONING_MODEL.replace(".2", "").replace(".1", ""),  # Remove version suffix
                        base_url="http://localhost:11434",
                        temperature=0.7,
                    )
                else:
                    self.llm = Ollama(
                        model=LLMConfig.BASIC_MODEL.replace(".2", "").replace(".1", "").split(":")[0],  # Remove version suffix and size
                        base_url="http://localhost:11434",
                        temperature=0.7,
                    )
            except (ImportError, Exception) as e:
                # If Ollama fails, try OpenAI
                try:
                    from langchain_openai import ChatOpenAI
                    if use_reasoning_llm:
                        self.llm = ChatOpenAI(
                            model=LLMConfig.REASONING_MODEL,
                            base_url=LLMConfig.REASONING_BASE_URL,
                            api_key=LLMConfig.REASONING_API_KEY,
                            temperature=0.7,
                        )
                    else:
                        self.llm = ChatOpenAI(
                            model=LLMConfig.BASIC_MODEL,
                            base_url=LLMConfig.BASIC_BASE_URL,
                            api_key=LLMConfig.BASIC_API_KEY,
                            temperature=0.7,
                        )
                except ImportError:
                    # If all else fails, create a dummy LLM
                    from langchain.llms.base import LLM

                    class DummyLLM(LLM):
                        def _call(self, prompt: str, **kwargs) -> str:
                            return "I'm sorry, but no language model is available. Please make sure Ollama is installed or set up an OpenAI API key."

                        @property
                        def _identifying_params(self) -> Dict[str, Any]:
                            return {}

                        @property
                        def _llm_type(self) -> str:
                            return "dummy"

                    self.llm = DummyLLM()

        # Load system prompt
        self.system_prompt = format_prompt(agent_type)
        self.messages.append(SystemMessage(content=self.system_prompt))

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
            # Check if the LLM is a ChatModel or a regular LLM
            if hasattr(self.llm, 'invoke') and callable(getattr(self.llm, 'invoke')):
                # ChatModel interface (like ChatOpenAI)
                response = self.llm.invoke(self.messages)
                response_text = response.content if hasattr(response, 'content') else str(response)
            else:
                # Regular LLM interface (like Ollama)
                # Convert messages to a prompt string
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
            fallback_response = "I'm sorry, but I encountered an error while processing your request. Please try again or check if the language model is available."
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

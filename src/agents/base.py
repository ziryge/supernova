"""
Base agent class for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.llms import Ollama

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

        # Initialize the LLM
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
        except Exception as e:
            # If Ollama initialization fails, print error and create a simple error-returning LLM
            print(f"Error initializing Ollama: {str(e)}")
            from langchain.llms.base import LLM

            class ErrorLLM(LLM):
                def _call(self, prompt: str, **kwargs) -> str:
                    return "I'm sorry, but I couldn't connect to Ollama. Please make sure Ollama is running."

                @property
                def _identifying_params(self) -> Dict[str, Any]:
                    return {}

                @property
                def _llm_type(self) -> str:
                    return "error"

            # Initialize the error LLM
            self.llm = ErrorLLM()

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
            # Convert messages to a prompt string for Ollama
            prompt = self._messages_to_prompt(self.messages)

            # Get response from Ollama
            response_text = self.llm(prompt)

            # Add the response to the conversation history
            self.add_message("ai", response_text)

            return response_text
        except Exception as e:
            # Handle errors gracefully
            error_message = f"Error getting response from Ollama: {str(e)}"
            print(error_message)

            # Add a fallback response to the conversation history
            fallback_response = "I'm sorry, but I encountered an error while processing your request. Please make sure Ollama is running properly."
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

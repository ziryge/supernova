"""
Base agent class for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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

        # Get the response from the LLM
        response = self.llm.invoke(self.messages)

        # Add the response to the conversation history
        self.add_message("ai", response.content)

        return response.content

    def reset(self) -> None:
        """Reset the agent's conversation history."""
        self.messages = [SystemMessage(content=self.system_prompt)]

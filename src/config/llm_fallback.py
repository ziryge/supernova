"""
LLM fallback configuration for SuperNova AI.
This module provides fallback mechanisms when Ollama is not available.
"""

import os
import time
import socket
import requests
from typing import Dict, Any, Optional, List, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if we're running on Streamlit Cloud
IS_STREAMLIT_CLOUD = os.environ.get('STREAMLIT_SHARING_MODE') == 'streamlit' or 'STREAMLIT_RUNTIME' in os.environ

def is_ollama_available() -> bool:
    """
    Check if Ollama is available by trying to connect to the Ollama API.
    
    Returns:
        bool: True if Ollama is available, False otherwise
    """
    try:
        # Try to connect to Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except (requests.RequestException, socket.error):
        return False

def wait_for_ollama(max_attempts: int = 3, delay: int = 5) -> bool:
    """
    Wait for Ollama to become available.
    
    Args:
        max_attempts: Maximum number of attempts to check if Ollama is available
        delay: Delay in seconds between attempts
        
    Returns:
        bool: True if Ollama became available, False otherwise
    """
    logger.info("Waiting for Ollama to become available...")
    
    for attempt in range(max_attempts):
        if is_ollama_available():
            logger.info("Ollama is available!")
            return True
        
        logger.info(f"Ollama not available yet. Attempt {attempt + 1}/{max_attempts}. Waiting {delay} seconds...")
        time.sleep(delay)
    
    logger.warning("Ollama is not available after maximum attempts")
    return False

def get_llm_config() -> Dict[str, Any]:
    """
    Get the LLM configuration based on availability.
    
    Returns:
        Dict[str, Any]: LLM configuration
    """
    # Check if OpenAI API key is available
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    # Check if Anthropic API key is available
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    # If we're on Streamlit Cloud, try to use Ollama first
    if IS_STREAMLIT_CLOUD:
        # Try to wait for Ollama to become available
        if wait_for_ollama():
            logger.info("Using Ollama on Streamlit Cloud")
            return {
                "type": "ollama",
                "model": "llama3",
                "url": "http://localhost:11434",
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2048
            }
        
        # If Ollama is not available and we have OpenAI API key, use OpenAI
        if openai_api_key:
            logger.info("Falling back to OpenAI on Streamlit Cloud")
            return {
                "type": "openai",
                "model": "gpt-3.5-turbo",
                "api_key": openai_api_key,
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2048
            }
        
        # If we have Anthropic API key, use Anthropic
        if anthropic_api_key:
            logger.info("Falling back to Anthropic on Streamlit Cloud")
            return {
                "type": "anthropic",
                "model": "claude-3-haiku-20240307",
                "api_key": anthropic_api_key,
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2048
            }
        
        # If no API keys are available, use a dummy LLM that returns a message
        logger.warning("No LLM available on Streamlit Cloud. Using dummy LLM.")
        return {
            "type": "dummy",
            "message": "No language model is available. Please set up an OpenAI or Anthropic API key in the Streamlit Cloud secrets."
        }
    
    # If we're not on Streamlit Cloud, check if Ollama is available locally
    if is_ollama_available():
        logger.info("Using local Ollama")
        return {
            "type": "ollama",
            "model": "llama3",
            "url": "http://localhost:11434",
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2048
        }
    
    # If Ollama is not available locally and we have OpenAI API key, use OpenAI
    if openai_api_key:
        logger.info("Falling back to OpenAI locally")
        return {
            "type": "openai",
            "model": "gpt-3.5-turbo",
            "api_key": openai_api_key,
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2048
        }
    
    # If we have Anthropic API key, use Anthropic
    if anthropic_api_key:
        logger.info("Falling back to Anthropic locally")
        return {
            "type": "anthropic",
            "model": "claude-3-haiku-20240307",
            "api_key": anthropic_api_key,
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2048
        }
    
    # If no API keys are available, use a dummy LLM that returns a message
    logger.warning("No LLM available locally. Using dummy LLM.")
    return {
        "type": "dummy",
        "message": "No language model is available. Please install Ollama or set up an OpenAI or Anthropic API key."
    }

def create_llm(config: Dict[str, Any] = None):
    """
    Create an LLM based on the configuration.
    
    Args:
        config: LLM configuration (if None, will be determined automatically)
        
    Returns:
        LLM instance
    """
    if config is None:
        config = get_llm_config()
    
    llm_type = config.get("type", "")
    
    if llm_type == "ollama":
        try:
            from langchain_community.llms import Ollama
            return Ollama(
                model=config.get("model", "llama3"),
                base_url=config.get("url", "http://localhost:11434"),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 0.9),
                num_predict=config.get("max_tokens", 2048)
            )
        except ImportError:
            logger.error("Failed to import Ollama. Make sure langchain_community is installed.")
            return create_dummy_llm("Failed to import Ollama. Make sure langchain_community is installed.")
    
    elif llm_type == "openai":
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=config.get("model", "gpt-3.5-turbo"),
                openai_api_key=config.get("api_key"),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 0.9),
                max_tokens=config.get("max_tokens", 2048)
            )
        except ImportError:
            logger.error("Failed to import OpenAI. Make sure langchain_openai is installed.")
            return create_dummy_llm("Failed to import OpenAI. Make sure langchain_openai is installed.")
    
    elif llm_type == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=config.get("model", "claude-3-haiku-20240307"),
                anthropic_api_key=config.get("api_key"),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 0.9),
                max_tokens=config.get("max_tokens", 2048)
            )
        except ImportError:
            logger.error("Failed to import Anthropic. Make sure langchain_anthropic is installed.")
            return create_dummy_llm("Failed to import Anthropic. Make sure langchain_anthropic is installed.")
    
    else:
        # Dummy LLM
        return create_dummy_llm(config.get("message", "No language model is available."))

def create_dummy_llm(message: str):
    """
    Create a dummy LLM that returns a fixed message.
    
    Args:
        message: Message to return
        
    Returns:
        Dummy LLM instance
    """
    from langchain.llms.base import LLM
    
    class DummyLLM(LLM):
        message: str = message
        
        def _call(self, prompt: str, **kwargs) -> str:
            return f"{self.message}\n\nYour prompt was: {prompt[:100]}..."
        
        @property
        def _identifying_params(self) -> Dict[str, Any]:
            return {"message": self.message}
        
        @property
        def _llm_type(self) -> str:
            return "dummy"
    
    return DummyLLM(message=message)

# Create a global LLM instance
llm = create_llm()

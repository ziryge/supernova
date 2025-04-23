"""
Environment configuration for SuperNova AI.
"""

import os
from dotenv import load_dotenv

# Check for DuckDuckGo search availability
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

# Load environment variables
load_dotenv()

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
APP_ENV = os.getenv("APP_ENV", "development")

# LLM Configuration
class LLMConfig:
    """Configuration for LLM models."""

    # Reasoning LLM (for complex reasoning tasks)
    REASONING_API_KEY = os.getenv("REASONING_API_KEY", "not-needed-for-ollama")
    REASONING_BASE_URL = os.getenv("REASONING_BASE_URL", "http://localhost:11434/v1")
    REASONING_MODEL = os.getenv("REASONING_MODEL", "llama3.2")

    # Basic LLM (for simpler tasks)
    BASIC_API_KEY = os.getenv("BASIC_API_KEY", "not-needed-for-ollama")
    BASIC_BASE_URL = os.getenv("BASIC_BASE_URL", "http://localhost:11434/v1")
    BASIC_MODEL = os.getenv("BASIC_MODEL", "llama3.1:8b")

    # Vision-Language LLM (for tasks involving images)
    VL_API_KEY = os.getenv("VL_API_KEY", "not-needed-for-ollama")
    VL_BASE_URL = os.getenv("VL_BASE_URL", "http://localhost:11434/v1")
    VL_MODEL = os.getenv("VL_MODEL", "llama3.2-vision")

# Tool Configuration
class ToolConfig:
    """Configuration for external tools."""

    # Search tools
    JINA_API_KEY = os.getenv("JINA_API_KEY", "")

    # Browser configuration
    CHROME_INSTANCE_PATH = os.getenv("CHROME_INSTANCE_PATH", "")

# Validate configuration
def validate_config():
    """Validate the configuration."""
    if not LLMConfig.REASONING_MODEL:
        print("Warning: REASONING_MODEL is not set. Using default model.")

    if not LLMConfig.BASIC_MODEL:
        print("Warning: BASIC_MODEL is not set. Using default model.")

    if not LLMConfig.VL_MODEL:
        print("Warning: VL_MODEL is not set. Using default model.")

    # Check for search capabilities
    if not DDGS_AVAILABLE and DEBUG:
        print("Warning: DuckDuckGo search is not available. Web search functionality will be limited.")

# Run validation
validate_config()

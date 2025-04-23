"""
Agent configuration for SuperNova AI.
"""

# Team composition
TEAM_CONFIG = {
    "supervisor": {
        "name": "Supervisor",
        "description": "Coordinates the team and delegates tasks",
        "emoji": "🧠",
    },
    "researcher": {
        "name": "Researcher",
        "description": "Gathers and analyzes information",
        "emoji": "🔍",
    },
    "coder": {
        "name": "Coder",
        "description": "Handles code generation and execution",
        "emoji": "💻",
    },
    "browser": {
        "name": "Browser",
        "description": "Performs web browsing and information retrieval",
        "emoji": "🌐",
    },
    "file_manager": {
        "name": "File Manager",
        "description": "Handles file operations",
        "emoji": "📁",
    },
}

# Agent system prompts
SYSTEM_PROMPTS = {
    "supervisor": "You are the Supervisor, responsible for coordinating the team and delegating tasks.",
    "researcher": "You are the Researcher, responsible for gathering and analyzing information.",
    "coder": "You are the Coder, responsible for writing and executing code.",
    "browser": "You are the Browser, responsible for web browsing and information retrieval.",
    "file_manager": "You are the File Manager, responsible for handling file operations.",
}

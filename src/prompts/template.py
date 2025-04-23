"""
Template engine for agent prompts.
"""

import os
import datetime
from pathlib import Path
from typing import Dict, Any

def load_prompt_template(template_name: str) -> str:
    """
    Load a prompt template from a file.
    
    Args:
        template_name: Name of the template file (without extension)
        
    Returns:
        The template content as a string
    """
    base_dir = Path(__file__).parent
    template_path = base_dir / f"{template_name}.md"
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

def format_prompt(template_name: str, variables: Dict[str, Any] = None) -> str:
    """
    Format a prompt template with variables.
    
    Args:
        template_name: Name of the template file (without extension)
        variables: Dictionary of variables to substitute in the template
        
    Returns:
        The formatted prompt as a string
    """
    template = load_prompt_template(template_name)
    
    if variables is None:
        variables = {}
    
    # Add default variables
    default_vars = {
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "current_date": datetime.datetime.now().strftime("%Y-%m-%d"),
    }
    
    # Merge default variables with provided variables
    variables = {**default_vars, **variables}
    
    # Format the template
    return template.format(**variables)

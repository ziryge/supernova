"""
File manager agent for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAgent
from ..tools.file_operations import file_operations

class FileManagerAgent(BaseAgent):
    """File manager agent that handles file operations."""

    def __init__(self):
        """Initialize the file manager agent."""
        super().__init__("file_manager", use_reasoning_llm=False)

    def create_file(self, content: str, file_path: str, file_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a file with the given content.

        Args:
            content: Content to write to the file
            file_path: Path to the file
            file_type: Type of file (markdown, python, etc.)

        Returns:
            A dictionary containing the result of the operation
        """
        # Format the content based on the file type
        if file_type:
            formatted_content = self._format_content(content, file_type)
        else:
            formatted_content = content

        # Ask the LLM to review and improve the content
        prompt = f"I need to create a file at '{file_path}' with the following content:\n\n{formatted_content}\n\nPlease review this content and suggest any improvements or formatting changes to make it more readable and professional."

        response = self.get_response(prompt)

        # Extract the improved content from the response
        improved_content = self._extract_content(response)

        # Write the file
        result = file_operations.write_file(file_path, improved_content or formatted_content)

        return {
            "file_path": file_path,
            "content": improved_content or formatted_content,
            "file_type": file_type,
            "result": result,
            "suggestions": response,
        }

    def read_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read a file and analyze its content.

        Args:
            file_path: Path to the file

        Returns:
            A dictionary containing the file content and analysis
        """
        # Read the file
        result = file_operations.read_file(file_path)

        if result["status"] == "error":
            return result

        content = result["content"]

        # Ask the LLM to analyze the content
        prompt = f"I need to analyze the content of the file at '{file_path}':\n\n{content}\n\nPlease provide a brief summary of this file, including its purpose, structure, and key components."

        analysis = self.get_response(prompt)

        return {
            "file_path": file_path,
            "content": content,
            "analysis": analysis,
            "result": result,
        }

    def organize_files(self, directory: str) -> Dict[str, Any]:
        """
        Organize files in a directory.

        Args:
            directory: Directory to organize

        Returns:
            A dictionary containing the organization plan
        """
        # List files in the directory
        result = file_operations.list_files(directory)

        if result["status"] == "error":
            return result

        files = result["files"]

        # Format the file list
        formatted_files = ""
        for file in files:
            formatted_files += f"{file['name']} - {'Directory' if file['is_dir'] else 'File'} - {file['size']} bytes\n"

        # Ask the LLM to suggest an organization plan
        prompt = f"I need to organize the files in the directory '{directory}':\n\n{formatted_files}\n\nPlease suggest a plan for organizing these files, including any directories that should be created, files that should be renamed, or files that should be moved."

        plan = self.get_response(prompt)

        return {
            "directory": directory,
            "files": files,
            "plan": plan,
            "result": result,
        }

    def _format_content(self, content: str, file_type: str) -> str:
        """
        Format content based on the file type.

        Args:
            content: Content to format
            file_type: Type of file

        Returns:
            Formatted content as a string
        """
        if file_type.lower() == "markdown":
            # Ask the LLM to format the content as markdown
            prompt = f"I need to format the following content as markdown:\n\n{content}\n\nPlease format this content with proper markdown syntax, including headings, lists, code blocks, and other formatting as appropriate."

            response = self.get_response(prompt)

            return self._extract_content(response) or content

        elif file_type.lower() == "python":
            # Ask the LLM to format the content as Python code
            prompt = f"I need to format the following content as Python code:\n\n{content}\n\nPlease format this content with proper Python syntax, including docstrings, comments, and PEP 8 style guidelines."

            response = self.get_response(prompt)

            return self._extract_content(response) or content

        else:
            # No special formatting
            return content

    def _extract_content(self, response: str) -> str:
        """
        Extract formatted content from the response.

        Args:
            response: Response from the LLM

        Returns:
            Extracted content as a string
        """
        # Look for content blocks
        lines = response.split("\n")
        in_block = False
        current_block = []
        blocks = []

        for line in lines:
            if line.strip().startswith("```") and not in_block:
                in_block = True
                continue
            elif line.strip() == "```" and in_block:
                in_block = False
                blocks.append("\n".join(current_block))
                current_block = []
                continue

            if in_block:
                current_block.append(line)

        # If no blocks found, return the entire response
        if not blocks:
            return response

        # Return the longest block
        return max(blocks, key=len)

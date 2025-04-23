"""
Coder agent for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAgent
from ..tools.python_repl import python_repl

class CoderAgent(BaseAgent):
    """Coder agent that writes and executes code."""

    def __init__(self):
        """Initialize the coder agent."""
        super().__init__("coder", use_reasoning_llm=True)

    def write_code(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Write code to solve a task.

        Args:
            task: Task to solve
            context: Additional context for the task

        Returns:
            A dictionary containing the code and explanation
        """
        prompt = f"I need to write Python code to solve the following task:\n\n{task}"

        if context:
            prompt += f"\n\nAdditional context:\n{context}"

        prompt += "\n\nPlease write clean, efficient, and well-documented Python code to solve this task. Include comments to explain complex logic and provide a brief explanation of how the code works."

        response = self.get_response(prompt)

        # Extract the code from the response
        code = self._extract_code(response)
        explanation = self._extract_explanation(response, code)

        return {
            "task": task,
            "code": code,
            "explanation": explanation,
            "full_response": response,
        }

    def execute_code(self, code: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute Python code.

        Args:
            code: Python code to execute
            timeout: Timeout in seconds

        Returns:
            A dictionary containing the execution result
        """
        # Execute the code
        result = python_repl.execute(code, timeout)

        # Ask the LLM to analyze the result
        prompt = f"I executed the following Python code:\n\n```python\n{code}\n```\n\nExecution result:\n```\nStatus: {result['status']}\nOutput: {result.get('output', '')}\nError: {result.get('error', '')}\nResult: {result.get('result', 'None')}\n```\n\nPlease analyze the execution result and explain what happened. If there were errors, suggest how to fix them."

        analysis = self.get_response(prompt)

        return {
            "code": code,
            "execution_result": result,
            "analysis": analysis,
        }

    def debug_code(self, code: str, error: str) -> Dict[str, Any]:
        """
        Debug Python code.

        Args:
            code: Python code to debug
            error: Error message

        Returns:
            A dictionary containing the debugged code and explanation
        """
        prompt = f"I need to debug the following Python code that produced an error:\n\n```python\n{code}\n```\n\nError message:\n```\n{error}\n```\n\nPlease identify the issue, explain what's causing it, and provide a fixed version of the code."

        response = self.get_response(prompt)

        # Extract the debugged code from the response
        debugged_code = self._extract_code(response)
        explanation = self._extract_explanation(response, debugged_code)

        return {
            "original_code": code,
            "error": error,
            "debugged_code": debugged_code,
            "explanation": explanation,
            "full_response": response,
        }

    def _extract_code(self, response: str) -> str:
        """
        Extract code blocks from the response.

        Args:
            response: Response from the LLM

        Returns:
            Extracted code as a string
        """
        # Look for Python code blocks
        code_blocks = []
        lines = response.split("\n")
        in_code_block = False
        current_block = []

        for line in lines:
            if line.strip().startswith("```python") or line.strip() == "```python":
                in_code_block = True
                continue
            elif line.strip() == "```" and in_code_block:
                in_code_block = False
                code_blocks.append("\n".join(current_block))
                current_block = []
                continue

            if in_code_block:
                current_block.append(line)

        # If no Python code blocks found, look for generic code blocks
        if not code_blocks:
            in_code_block = False
            for line in lines:
                if line.strip() == "```" and not in_code_block:
                    in_code_block = True
                    continue
                elif line.strip() == "```" and in_code_block:
                    in_code_block = False
                    code_blocks.append("\n".join(current_block))
                    current_block = []
                    continue

                if in_code_block:
                    current_block.append(line)

        # If still no code blocks found, try to extract code based on indentation
        if not code_blocks:
            in_code_section = False
            for line in lines:
                if line.strip().startswith("def ") or line.strip().startswith("class "):
                    in_code_section = True
                    current_block.append(line)
                elif in_code_section and (line.startswith("    ") or line.strip() == ""):
                    current_block.append(line)
                elif in_code_section:
                    in_code_section = False
                    code_blocks.append("\n".join(current_block))
                    current_block = []

            if current_block:
                code_blocks.append("\n".join(current_block))

        # Return the longest code block
        if code_blocks:
            return max(code_blocks, key=len)

        return ""

    def _extract_explanation(self, response: str, code: str) -> str:
        """
        Extract explanation from the response.

        Args:
            response: Response from the LLM
            code: Extracted code

        Returns:
            Extracted explanation as a string
        """
        # Remove the code from the response
        explanation = response.replace(f"```python\n{code}\n```", "")
        explanation = explanation.replace(f"```\n{code}\n```", "")

        # Clean up the explanation
        explanation = explanation.strip()

        return explanation

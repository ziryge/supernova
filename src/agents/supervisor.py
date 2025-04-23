"""
Supervisor agent for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAgent

class SupervisorAgent(BaseAgent):
    """Supervisor agent that coordinates other agents."""

    def __init__(self):
        """Initialize the supervisor agent."""
        super().__init__("supervisor", use_reasoning_llm=True)

    def delegate_task(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Delegate a task to the appropriate agent.

        Args:
            task: Task to delegate
            context: Additional context for the task

        Returns:
            A dictionary containing the delegation decision
        """
        prompt = f"""I need to delegate the following task to a specialist:

{task}

"""

        if context:
            prompt += f"Additional context:\n{context}\n\n"

        prompt += """Which specialist should handle this task? Please provide your response in the following format:

**Reasoning:**
A detailed explanation of why you chose this specialist, considering the nature of the task and the specialist's expertise.

**Instructions for [Specialist Name]:**

1. **Clear Instructions:** Specific, actionable instructions for completing the task.
2. **Context:** Any relevant context or background information the specialist needs.
3. **Output Expectations:** Clear description of what the final output should look like.

**Additional Guidance:**
Any other information, tips, or considerations that might help the specialist complete the task effectively.

**Delegation Note:** A brief confirmation message for the specialist to acknowledge receipt of the task.

Choose from these specialists: Researcher, Coder, Browser, File Manager, or Sandbox.
"""

        response = self.get_response(prompt)

        # Parse the response to determine the chosen specialist
        specialist = self._parse_specialist(response)

        return {
            "specialist": specialist,
            "reasoning": response,
            "task": task,
            "context": context,
        }

    def evaluate_result(self, result: str, task: str) -> Dict[str, Any]:
        """
        Evaluate the result of a task.

        Args:
            result: Result to evaluate
            task: Original task

        Returns:
            A dictionary containing the evaluation
        """
        prompt = f"I need to evaluate the following result for the task:\n\nTask: {task}\n\nResult:\n{result}\n\nIs this result satisfactory? Does it fully address the task? What improvements could be made?"

        response = self.get_response(prompt)

        # Parse the response to determine if the result is satisfactory
        is_satisfactory = "satisfactory" in response.lower() or "sufficient" in response.lower()
        needs_improvement = "improvement" in response.lower() or "could be better" in response.lower()

        return {
            "is_satisfactory": is_satisfactory,
            "needs_improvement": needs_improvement,
            "evaluation": response,
            "task": task,
            "result": result,
        }

    def summarize_workflow(self, tasks: List[Dict[str, Any]]) -> str:
        """
        Summarize the workflow of completed tasks.

        Args:
            tasks: List of completed tasks

        Returns:
            A summary of the workflow
        """
        prompt = "I need to summarize the workflow of the following completed tasks:\n\n"

        for i, task in enumerate(tasks, 1):
            prompt += f"Task {i}: {task['task']}\n"
            prompt += f"Specialist: {task['specialist']}\n"
            prompt += f"Result: {task['result'][:100]}...\n\n"

        prompt += "Please provide a concise summary of the workflow, highlighting the key steps and results."

        return self.get_response(prompt)

    def _parse_specialist(self, response: str) -> str:
        """
        Parse the specialist from the response.

        Args:
            response: Response from the LLM

        Returns:
            The chosen specialist
        """
        response_lower = response.lower()

        if "researcher" in response_lower:
            return "researcher"
        elif "coder" in response_lower:
            return "coder"
        elif "browser" in response_lower or "web" in response_lower or "website" in response_lower or "browse" in response_lower:
            return "browser"
        elif "file manager" in response_lower or "file_manager" in response_lower:
            return "file_manager"
        elif "sandbox" in response_lower or "execute" in response_lower or "command" in response_lower or "terminal" in response_lower or "shell" in response_lower:
            return "sandbox"
        else:
            return "unknown"

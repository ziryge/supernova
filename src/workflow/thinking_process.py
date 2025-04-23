"""
Thinking process module for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
import time
import json

class ThinkingProcess:
    """Class to track and manage the agent's thinking process."""

    # Define thinking modes
    NORMAL_THINKING = "normal"
    DEEP_THINKING = "deep"
    SUPER_DEEP_THINKING = "super_deep"

    def __init__(self, thinking_mode=NORMAL_THINKING):
        """Initialize the thinking process.

        Args:
            thinking_mode: The level of detail in thinking process (normal, deep, super_deep)
        """
        self.steps = []
        self.current_step = None
        self.start_time = time.time()
        self.artifacts = []
        self.links = []
        self.files = []
        self.plan = []
        self.terminal_output = []
        self.thinking_mode = thinking_mode

    def start_thinking(self, query: str, thinking_mode=None) -> None:
        """
        Start a new thinking process.

        Args:
            query: The user query that initiated the thinking process
            thinking_mode: Optional override for the thinking mode
        """
        self.steps = []
        self.current_step = None
        self.start_time = time.time()
        self.artifacts = []
        self.links = []
        self.files = []
        self.plan = []
        self.terminal_output = []

        # Update thinking mode if provided
        if thinking_mode:
            self.thinking_mode = thinking_mode

        # Add the initial step
        self.add_step("query", {
            "content": query,
            "type": "user_query",
        })

        # Add thinking mode indicator
        if self.thinking_mode == self.DEEP_THINKING:
            self.add_thinking("Deep Thinking Mode activated. I'll provide more detailed reasoning and analysis.")
        elif self.thinking_mode == self.SUPER_DEEP_THINKING:
            self.add_thinking("Super Deep Thinking Mode activated. I'll provide extremely detailed reasoning, analysis, and alternative approaches.")

    def add_step(self, step_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a step to the thinking process.

        Args:
            step_type: Type of step (e.g., "thinking", "planning", "execution")
            content: Content of the step

        Returns:
            The created step
        """
        step = {
            "id": len(self.steps) + 1,
            "type": step_type,
            "content": content,
            "timestamp": time.time(),
            "elapsed": time.time() - self.start_time,
        }

        self.steps.append(step)
        self.current_step = step

        return step

    def add_thinking(self, thought: str, depth: int = 0) -> Dict[str, Any]:
        """
        Add a thinking step.

        Args:
            thought: The thought content
            depth: The depth level of the thought (0=normal, 1=deeper, 2=deepest)

        Returns:
            The created step
        """
        # Determine if we should enhance the thought based on thinking mode
        enhanced_thought = thought
        thought_type = "thought"

        # Only enhance if depth is 0 (initial thought)
        if depth == 0:
            if self.thinking_mode == self.DEEP_THINKING and not thought.startswith("Deep Analysis:"):
                # Add a deeper level of thinking for Deep Thinking mode
                thought_type = "deep_thought"
                enhanced_thought = f"{thought}\n\nDeep Analysis: I'll analyze this further by considering multiple perspectives and potential implications."

            elif self.thinking_mode == self.SUPER_DEEP_THINKING and not thought.startswith("Super Deep Analysis:"):
                # Add an even deeper level of thinking for Super Deep Thinking mode
                thought_type = "super_deep_thought"
                enhanced_thought = f"{thought}\n\nSuper Deep Analysis: I'll perform an extensive analysis by considering multiple perspectives, potential implications, alternative approaches, and edge cases. I'll also evaluate the confidence level of my reasoning."

        return self.add_step("thinking", {
            "content": enhanced_thought,
            "type": thought_type,
            "depth": depth,
        })

    def add_planning(self, plan: List[str]) -> Dict[str, Any]:
        """
        Add a planning step.

        Args:
            plan: The plan steps

        Returns:
            The created step
        """
        self.plan = plan

        return self.add_step("planning", {
            "content": plan,
            "type": "plan",
        })

    def add_execution(self, action: str, result: Any) -> Dict[str, Any]:
        """
        Add an execution step.

        Args:
            action: The action performed
            result: The result of the action

        Returns:
            The created step
        """
        return self.add_step("execution", {
            "action": action,
            "result": result,
            "type": "execution",
        })

    def add_artifact(self, artifact_type: str, content: Any) -> Dict[str, Any]:
        """
        Add an artifact.

        Args:
            artifact_type: Type of artifact (e.g., "link", "file", "image")
            content: Content of the artifact

        Returns:
            The created artifact
        """
        artifact = {
            "id": len(self.artifacts) + 1,
            "type": artifact_type,
            "content": content,
            "timestamp": time.time(),
            "step_id": self.current_step["id"] if self.current_step else None,
        }

        self.artifacts.append(artifact)

        # Add to specific collections
        if artifact_type == "link":
            self.links.append(artifact)
        elif artifact_type == "file":
            self.files.append(artifact)

        return artifact

    def add_link(self, url: str, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a link artifact.

        Args:
            url: URL of the link
            title: Title of the link
            description: Description of the link

        Returns:
            The created artifact
        """
        return self.add_artifact("link", {
            "url": url,
            "title": title or url,
            "description": description or "",
        })

    def add_file(self, path: str, content: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a file artifact.

        Args:
            path: Path to the file
            content: Content of the file
            description: Description of the file

        Returns:
            The created artifact
        """
        return self.add_artifact("file", {
            "path": path,
            "content": content,
            "description": description or "",
        })

    def add_deep_thinking(self, thought: str, perspectives: List[str] = None) -> Dict[str, Any]:
        """
        Add a deep thinking step with multiple perspectives.

        Args:
            thought: The base thought content
            perspectives: List of different perspectives to consider

        Returns:
            The created step
        """
        if not perspectives:
            perspectives = [
                "Logical perspective",
                "Creative perspective",
                "Critical perspective",
                "Practical perspective"
            ]

        # Create the enhanced thought with perspectives
        enhanced_thought = f"Deep Analysis: {thought}\n\n"
        for perspective in perspectives:
            enhanced_thought += f"**{perspective}**: Considering this from a {perspective.lower()} viewpoint...\n"

        # Add the deep thinking step
        return self.add_thinking(enhanced_thought, depth=1)

    def add_super_deep_thinking(self, thought: str, analysis_points: List[str] = None) -> Dict[str, Any]:
        """
        Add a super deep thinking step with comprehensive analysis.

        Args:
            thought: The base thought content
            analysis_points: List of analysis points to consider

        Returns:
            The created step
        """
        if not analysis_points:
            analysis_points = [
                "Multiple perspectives",
                "Potential implications",
                "Alternative approaches",
                "Edge cases",
                "Confidence assessment",
                "Potential challenges",
                "Success criteria"
            ]

        # Create the enhanced thought with detailed analysis
        enhanced_thought = f"Super Deep Analysis: {thought}\n\n"
        for point in analysis_points:
            enhanced_thought += f"**{point}**: Analyzing {point.lower()} in depth...\n"

        # Add the super deep thinking step
        return self.add_thinking(enhanced_thought, depth=2)

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the thinking process.

        Returns:
            A dictionary containing the summary
        """
        return {
            "steps": self.steps,
            "artifacts": self.artifacts,
            "links": self.links,
            "files": self.files,
            "plan": self.plan,
            "terminal_output": self.terminal_output,
            "thinking_mode": self.thinking_mode,
            "elapsed": time.time() - self.start_time,
        }

    def add_terminal_output(self, output: str) -> Dict[str, Any]:
        """
        Add terminal output to the thinking process.

        Args:
            output: The terminal output to add

        Returns:
            The created step
        """
        # Add the output to the terminal output list
        self.terminal_output.append({
            "content": output,
            "timestamp": time.time(),
            "elapsed": time.time() - self.start_time,
        })

        # Also add it as a thinking step for visibility
        return self.add_step("terminal", {
            "content": output,
            "type": "terminal_output",
        })

    def to_json(self) -> str:
        """
        Convert the thinking process to JSON.

        Returns:
            JSON string representation of the thinking process
        """
        return json.dumps(self.get_summary(), indent=2)

    def from_json(self, json_str: str) -> None:
        """
        Load the thinking process from JSON.

        Args:
            json_str: JSON string representation of the thinking process
        """
        data = json.loads(json_str)

        self.steps = data.get("steps", [])
        self.artifacts = data.get("artifacts", [])
        self.links = data.get("links", [])
        self.files = data.get("files", [])
        self.plan = data.get("plan", [])
        self.terminal_output = data.get("terminal_output", [])
        self.start_time = time.time() - data.get("elapsed", 0)

        if self.steps:
            self.current_step = self.steps[-1]

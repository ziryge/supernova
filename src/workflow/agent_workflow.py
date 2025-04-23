"""
Agent workflow for SuperNova AI.
"""

import time
from typing import Dict, Any, List, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from ..agents import SupervisorAgent, ResearcherAgent, CoderAgent, FileManagerAgent, BrowserAgent, OpenaBrowserAgent, StreamlitBrowserAgent, SandboxAgent
from ..config.env import DEBUG
from .thinking_process import ThinkingProcess
from ..utils import TerminalCapture

class AgentWorkflow:
    """Agent workflow that coordinates multiple agents."""

    def __init__(self, debug: bool = False, use_enhanced_browser: bool = True, thinking_mode: str = ThinkingProcess.NORMAL_THINKING):
        """
        Initialize the agent workflow.

        Args:
            debug: Whether to enable debug mode
            use_enhanced_browser: Whether to use the enhanced SuperNova browser
            thinking_mode: The level of detail in thinking process (normal, deep, super_deep)
        """
        self.debug = debug
        self.use_enhanced_browser = use_enhanced_browser
        self.thinking_mode = thinking_mode

        # Initialize agents
        self.supervisor = SupervisorAgent()
        self.researcher = ResearcherAgent()
        self.coder = CoderAgent()
        self.file_manager = FileManagerAgent()
        self.sandbox = SandboxAgent()

        # Initialize browser agent (either standard, enhanced, or Streamlit-compatible)
        # Check if we're running in Streamlit Cloud
        import os
        is_streamlit_cloud = os.environ.get('STREAMLIT_SHARING_MODE') == 'streamlit' or 'STREAMLIT_RUNTIME' in os.environ

        if is_streamlit_cloud:
            # Use Streamlit-compatible browser agent in Streamlit Cloud
            self.browser = StreamlitBrowserAgent()
            if self.debug:
                print("Using Streamlit-compatible browser agent for Streamlit Cloud")
        elif use_enhanced_browser:
            # Use enhanced browser agent
            self.browser = OpenaBrowserAgent()
            if self.debug:
                print("Using enhanced SuperNova browser agent")
        else:
            # Use standard browser agent
            self.browser = BrowserAgent()
            if self.debug:
                print("Using standard browser agent")

        # Initialize workflow state
        self.messages = []
        self.tasks = []
        self.current_task = None

        # Initialize thinking process with the specified mode
        self.thinking = ThinkingProcess(thinking_mode=thinking_mode)

        if self.debug:
            print(f"Using thinking mode: {thinking_mode}")

    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Run the agent workflow.

        Args:
            user_input: User input to process

        Returns:
            A dictionary containing the workflow result
        """
        # Define a callback function to capture terminal output
        def capture_terminal_output(text: str):
            # Add the terminal output to the thinking process
            self.thinking.add_terminal_output(text.strip())

        # Start capturing terminal output
        with TerminalCapture(capture_terminal_output):
            # Start the thinking process with the current thinking mode
            self.thinking.start_thinking(user_input, thinking_mode=self.thinking_mode)

            # Add user input to messages
            self.messages.append(HumanMessage(content=user_input))

            # Think about the task with appropriate depth
            initial_thought = "Analyzing the user's request to determine the best specialist for this task."
            self.thinking.add_thinking(initial_thought)

            # Add deeper thinking based on the mode
            if self.thinking_mode == ThinkingProcess.DEEP_THINKING:
                self.thinking.add_deep_thinking("I need to carefully analyze this request to determine which specialist has the right expertise.", [
                    "Task requirements",
                    "Required expertise",
                    "Potential challenges",
                    "Success criteria"
                ])
            elif self.thinking_mode == ThinkingProcess.SUPER_DEEP_THINKING:
                self.thinking.add_super_deep_thinking("I need to thoroughly analyze this request from multiple angles to ensure optimal specialist selection.")

            # Delegate the task to the appropriate agent
            delegation = self.supervisor.delegate_task(user_input)
            specialist = delegation["specialist"]

            # Record the delegation reasoning with appropriate depth
            delegation_thought = f"I've decided to delegate this task to the {specialist.capitalize()} specialist."
            self.thinking.add_thinking(delegation_thought)

            # Add deeper delegation reasoning based on the mode
            if self.thinking_mode == ThinkingProcess.DEEP_THINKING:
                self.thinking.add_deep_thinking(f"Let me analyze why the {specialist.capitalize()} specialist is the best choice for this task.", [
                    "Specialist capabilities",
                    "Task alignment",
                    "Expected outcomes",
                    "Alternative specialists considered"
                ])
            elif self.thinking_mode == ThinkingProcess.SUPER_DEEP_THINKING:
                self.thinking.add_super_deep_thinking(f"I need to thoroughly justify my selection of the {specialist.capitalize()} specialist and consider all implications of this delegation decision.")

            # Add the delegation reasoning as a planning step
            plan_lines = delegation['reasoning'].split('\n')
            # Filter out empty lines and format as a plan
            plan = [line.strip() for line in plan_lines if line.strip()]
            self.thinking.add_planning(plan)

            if self.debug:
                print(f"Delegating task to {specialist}...")
                print(f"Reasoning: {delegation['reasoning']}")

            # Process the task with the chosen specialist
            if specialist == "researcher":
                result = self._process_researcher_task(user_input)
            elif specialist == "coder":
                result = self._process_coder_task(user_input)
            elif specialist == "file_manager":
                result = self._process_file_manager_task(user_input)
            elif specialist == "browser":
                result = self._process_browser_task(user_input)
            elif specialist == "sandbox":
                result = self._process_sandbox_task(user_input)
            else:
                # Default to supervisor if specialist is unknown
                result = self._process_supervisor_task(user_input)

            # Add the result to messages
            self.messages.append(AIMessage(content=result))

            # Add final thinking step with appropriate depth
            final_thought = "Task completed. Here's the final result."
            self.thinking.add_thinking(final_thought)

            # Add deeper final thinking based on the mode
            if self.thinking_mode == ThinkingProcess.DEEP_THINKING:
                self.thinking.add_deep_thinking("Let me review the completed task and assess the quality of the result.", [
                    "Task fulfillment",
                    "Result quality",
                    "Potential improvements",
                    "Next steps"
                ])
            elif self.thinking_mode == ThinkingProcess.SUPER_DEEP_THINKING:
                self.thinking.add_super_deep_thinking("I need to thoroughly evaluate the completed task, the quality of the result, and consider potential follow-up actions.")

            # Return the workflow result
            return {
                "messages": self.messages,
                "tasks": self.tasks,
                "result": result,
                "thinking": self.thinking.get_summary(),
            }

    def _process_researcher_task(self, task: str) -> str:
        """
        Process a task with the researcher agent.

        Args:
            task: Task to process

        Returns:
            Result of the task
        """
        # Record the task
        self.current_task = {
            "task": task,
            "specialist": "researcher",
            "start_time": time.time(),
        }

        # Add thinking step
        self.thinking.add_thinking("I'll use the Researcher agent to search for information on this topic.")

        # Create a plan
        plan = [
            "Analyze the search query to identify key terms",
            "Perform a web search to gather relevant information",
            "Analyze and synthesize the search results",
            "Provide a comprehensive summary of the findings"
        ]
        self.thinking.add_planning(plan)

        # Execute the plan
        self.thinking.add_thinking("Executing the research plan...")

        # Perform web search
        self.thinking.add_thinking("Performing web search...")
        search_result = self.researcher.search(task)

        # Record any links found
        for result in search_result.get("results", []):
            if "url" in result:
                self.thinking.add_link(
                    url=result["url"],
                    title=result.get("title", "Search Result"),
                    description=result.get("content", "")[:100] + "..."
                )

        # Add execution result
        self.thinking.add_execution("web_search", {
            "query": task,
            "result_count": len(search_result.get("results", [])),
        })

        # Add thinking step
        self.thinking.add_thinking("Analyzing search results and preparing a comprehensive summary...")

        # Add the result to the task
        self.current_task["result"] = search_result["analysis"]
        self.current_task["end_time"] = time.time()
        self.tasks.append(self.current_task)

        return search_result["analysis"]

    def _process_coder_task(self, task: str) -> str:
        """
        Process a task with the coder agent.

        Args:
            task: Task to process

        Returns:
            Result of the task
        """
        # Record the task
        self.current_task = {
            "task": task,
            "specialist": "coder",
            "start_time": time.time(),
        }

        # Add thinking step
        self.thinking.add_thinking("I'll use the Coder agent to write and execute code for this task.")

        # Create a plan
        plan = [
            "Analyze the coding task requirements",
            "Write Python code to solve the problem",
            "Execute the code to test it",
            "Debug any errors if necessary",
            "Provide the final solution with explanation"
        ]
        self.thinking.add_planning(plan)

        # Write code
        self.thinking.add_thinking("Writing code to solve the task...")
        code_result = self.coder.write_code(task)

        # Add execution step
        self.thinking.add_execution("write_code", {
            "code_length": len(code_result["code"]) if code_result["code"] else 0,
        })

        # Add thinking step
        if code_result["code"]:
            self.thinking.add_thinking(f"Code written successfully. Here's the solution:\n\n```python\n{code_result['code']}\n```\n\nNow I'll execute the code to test it.")

            # Add file to thinking process
            code_filename = "solution.py"
            self.thinking.add_file(
                path=code_filename,
                content=code_result["code"],
                description="Python code solution"
            )

            # Execute the code
            self.thinking.add_thinking("Executing the code...")
            execution_result = self.coder.execute_code(code_result["code"])

            # Add execution step
            self.thinking.add_execution("execute_code", {
                "status": execution_result["execution_result"]["status"],
                "output_length": len(execution_result["execution_result"].get("output", ""))
            })

            # Debug the code if there was an error
            if execution_result["execution_result"]["status"] == "error":
                self.thinking.add_thinking(f"Execution failed with error:\n\n```\n{execution_result['execution_result']['error']}\n```\n\nI'll debug the code and fix the issues.")

                debug_result = self.coder.debug_code(
                    code_result["code"],
                    execution_result["execution_result"]["error"]
                )

                # Add execution step
                self.thinking.add_execution("debug_code", {
                    "debugged_code_length": len(debug_result["debugged_code"]) if debug_result["debugged_code"] else 0,
                })

                # Try executing the debugged code
                if debug_result["debugged_code"]:
                    self.thinking.add_thinking(f"Code debugged. Here's the fixed solution:\n\n```python\n{debug_result['debugged_code']}\n```\n\nExecuting the debugged code...")

                    # Update file in thinking process
                    self.thinking.add_file(
                        path=code_filename,
                        content=debug_result["debugged_code"],
                        description="Debugged Python code solution"
                    )

                    execution_result = self.coder.execute_code(debug_result["debugged_code"])

                    # Add execution step
                    self.thinking.add_execution("execute_debugged_code", {
                        "status": execution_result["execution_result"]["status"],
                        "output_length": len(execution_result["execution_result"].get("output", ""))
                    })

                    # Use the debugged code if successful
                    if execution_result["execution_result"]["status"] == "success":
                        self.thinking.add_thinking("Debugged code executed successfully!")
                        code_result["code"] = debug_result["debugged_code"]
                        code_result["explanation"] += f"\n\nDebug Notes: {debug_result['explanation']}"
                    else:
                        self.thinking.add_thinking(f"Debugged code still has issues:\n\n```\n{execution_result['execution_result']['error']}\n```")
            else:
                self.thinking.add_thinking("Code executed successfully!")

                if execution_result['execution_result'].get('output'):
                    self.thinking.add_thinking(f"Output:\n\n```\n{execution_result['execution_result']['output']}\n```")
        else:
            self.thinking.add_thinking("I wasn't able to write code for this task.")

        # Format the result
        result = f"# Code Solution\n\n```python\n{code_result['code']}\n```\n\n## Explanation\n\n{code_result['explanation']}"

        if "execution_result" in locals():
            result += f"\n\n## Execution Result\n\n"
            result += f"Status: {execution_result['execution_result']['status']}\n\n"

            if execution_result['execution_result'].get('output'):
                result += f"Output:\n```\n{execution_result['execution_result']['output']}\n```\n\n"

            if execution_result['execution_result'].get('error'):
                result += f"Error:\n```\n{execution_result['execution_result']['error']}\n```\n\n"

            result += f"Analysis: {execution_result['analysis']}"

        # Add final thinking step
        self.thinking.add_thinking("Task completed. Providing the final code solution with explanation.")

        # Add the result to the task
        self.current_task["result"] = result
        self.current_task["end_time"] = time.time()
        self.tasks.append(self.current_task)

        return result

    def _process_file_manager_task(self, task: str) -> str:
        """
        Process a task with the file manager agent.

        Args:
            task: Task to process

        Returns:
            Result of the task
        """
        # Record the task
        self.current_task = {
            "task": task,
            "specialist": "file_manager",
            "start_time": time.time(),
        }

        # Add thinking step
        self.thinking.add_thinking("I'll use the File Manager agent to handle file operations.")

        # Determine the file operation to perform
        if "create" in task.lower() or "write" in task.lower() or "save" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be a file creation task. I'll extract the file path and content.")

            # Create a plan
            plan = [
                "Extract the file path and content from the task",
                "Determine the file type",
                "Format the content appropriately",
                "Create the file",
                "Verify the file was created successfully"
            ]
            self.thinking.add_planning(plan)

            # Extract file path and content from the task
            self.thinking.add_thinking("Extracting file path and content...")
            file_path, content, file_type = self._extract_file_info(task)

            # Add execution step
            self.thinking.add_execution("extract_file_info", {
                "file_path": file_path,
                "file_type": file_type,
                "content_length": len(content) if content else 0
            })

            if file_path and content:
                # Add thinking step
                self.thinking.add_thinking(f"Creating file at {file_path} with {len(content)} characters of content...")

                # Create the file
                result = self.file_manager.create_file(content, file_path, file_type)

                # Add execution step
                self.thinking.add_execution("create_file", {
                    "file_path": result['file_path'],
                    "status": result['result']['status'],
                })

                # Add file to thinking process
                self.thinking.add_file(
                    path=result['file_path'],
                    content=result['content'][:500] + ('...' if len(result['content']) > 500 else ''),
                    description=f"File created with {len(result['content'])} characters of content"
                )

                # Add thinking step
                self.thinking.add_thinking(f"File created successfully at {result['file_path']}.")

                # Format the result
                formatted_result = f"# File Created\n\nFile: {result['file_path']}\n\n## Content\n\n```\n{result['content'][:500]}{'...' if len(result['content']) > 500 else ''}\n```\n\n## Notes\n\n{result['suggestions']}"
            else:
                # Add thinking step
                self.thinking.add_thinking("I couldn't determine the file path or content from the request.")

                formatted_result = "I couldn't determine the file path or content from your request. Please provide more specific information."

        elif "read" in task.lower() or "open" in task.lower() or "view" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be a file reading task. I'll extract the file path.")

            # Create a plan
            plan = [
                "Extract the file path from the task",
                "Read the file content",
                "Analyze the file content",
                "Provide a summary of the file"
            ]
            self.thinking.add_planning(plan)

            # Extract file path from the task
            self.thinking.add_thinking("Extracting file path...")
            file_path = self._extract_file_path(task)

            # Add execution step
            self.thinking.add_execution("extract_file_path", {
                "file_path": file_path
            })

            if file_path:
                # Add thinking step
                self.thinking.add_thinking(f"Reading file at {file_path}...")

                # Read the file
                result = self.file_manager.read_file(file_path)

                # Add execution step
                self.thinking.add_execution("read_file", {
                    "file_path": file_path,
                    "status": result['status'],
                    "size": result.get('size', 0) if result['status'] == 'success' else 0
                })

                # Format the result
                if result["status"] == "success":
                    # Add file to thinking process
                    self.thinking.add_file(
                        path=result['file_path'],
                        content=result['content'][:500] + ('...' if len(result['content']) > 500 else ''),
                        description=f"File read with {len(result['content'])} characters of content"
                    )

                    # Add thinking step
                    self.thinking.add_thinking(f"File read successfully. Analyzing content...")

                    formatted_result = f"# File Contents\n\nFile: {result['file_path']}\n\n```\n{result['content'][:500]}{'...' if len(result['content']) > 500 else ''}\n```\n\n## Analysis\n\n{result['analysis']}"
                else:
                    # Add thinking step
                    self.thinking.add_thinking(f"Error reading file: {result['error']}")

                    formatted_result = f"Error: {result['error']}"
            else:
                # Add thinking step
                self.thinking.add_thinking("I couldn't determine the file path from the request.")

                formatted_result = "I couldn't determine the file path from your request. Please provide more specific information."

        elif "organize" in task.lower() or "list" in task.lower() or "directory" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be a directory listing or organization task. I'll extract the directory path.")

            # Create a plan
            plan = [
                "Extract the directory path from the task",
                "List the files in the directory",
                "Analyze the directory structure",
                "Suggest an organization plan"
            ]
            self.thinking.add_planning(plan)

            # Extract directory path from the task
            self.thinking.add_thinking("Extracting directory path...")
            directory = self._extract_directory_path(task) or "."

            # Add execution step
            self.thinking.add_execution("extract_directory_path", {
                "directory": directory
            })

            # Add thinking step
            self.thinking.add_thinking(f"Listing files in directory {directory}...")

            # Organize the files
            result = self.file_manager.organize_files(directory)

            # Add execution step
            self.thinking.add_execution("list_directory", {
                "directory": directory,
                "status": result['status'],
                "file_count": len(result.get('files', [])) if result['status'] == 'success' else 0
            })

            # Format the result
            if result["status"] == "success":
                # Add thinking step
                self.thinking.add_thinking(f"Found {len(result['files'])} files in directory {directory}. Creating organization plan...")

                # Add files to thinking process
                for file in result["files"]:
                    if not file['is_dir']:
                        self.thinking.add_file(
                            path=file['path'],
                            description=f"File in directory {directory}, size: {file['size']} bytes"
                        )

                formatted_result = f"# Directory Contents\n\nDirectory: {result['directory']}\n\n## Files\n\n"

                for file in result["files"]:
                    formatted_result += f"- {file['name']} ({'Directory' if file['is_dir'] else 'File'}, {file['size']} bytes)\n"

                formatted_result += f"\n## Organization Plan\n\n{result['plan']}"
            else:
                # Add thinking step
                self.thinking.add_thinking(f"Error listing directory: {result['error']}")

                formatted_result = f"Error: {result['error']}"

        else:
            # Add thinking step
            self.thinking.add_thinking("I'm not sure what file operation is being requested. I'll ask the Supervisor for guidance.")

            # Default to supervisor if operation is unknown
            return self._process_supervisor_task(task)

        # Add the result to the task
        self.current_task["result"] = formatted_result
        self.current_task["end_time"] = time.time()
        self.tasks.append(self.current_task)

        return formatted_result

    def _process_browser_task(self, task: str) -> str:
        """
        Process a task with the browser agent.

        Args:
            task: Task to process

        Returns:
            Result of the task
        """
        # Record the task
        self.current_task = {
            "task": task,
            "specialist": "browser",
            "start_time": time.time(),
        }

        # Add thinking step
        self.thinking.add_thinking("I'll use the Browser agent to navigate the web and extract information.")

        # Determine if this is a search or direct browsing task
        if "search" in task.lower() and "browse" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be a search and browse task. I'll extract the search query first.")

            # Create a plan
            plan = [
                "Extract the search query from the task",
                "Perform a web search to find relevant pages",
                "Browse the top search result",
                "Analyze the content of the page",
                "Provide a comprehensive summary"
            ]
            self.thinking.add_planning(plan)

            # Extract the search query
            self.thinking.add_thinking("Extracting search query...")
            prompt = f"I need to extract a search query from the following task:\n\n{task}\n\nPlease provide just the search query without any additional text."
            query = self.supervisor.get_response(prompt).strip()

            # Add execution step
            self.thinking.add_execution("extract_query", {
                "query": query
            })

            # Search and browse
            self.thinking.add_thinking(f"Searching for: '{query}' and browsing the top result...")
            result = self.browser.search_and_browse(query)

            # Record the browsed URL
            self.thinking.add_link(
                url=result['browsed_url'],
                title=result.get('browse_result', {}).get('title', result['browsed_url']),
                description="Top search result that was browsed"
            )

            # Add execution step
            self.thinking.add_execution("search_and_browse", {
                "query": query,
                "url": result['browsed_url'],
                "title": result.get('browse_result', {}).get('title', "")
            })

            # Add thinking step
            self.thinking.add_thinking("Analyzing the content and preparing a summary...")

            formatted_result = f"# Search and Browse Results\n\nQuery: {query}\n\nURL: {result['browsed_url']}\n\n## Analysis\n\n{result['analysis']}"

        elif "browse" in task.lower() or "visit" in task.lower() or "go to" in task.lower() or "open" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be a direct browsing task. I'll extract the URL to visit.")

            # Create a plan
            plan = [
                "Extract the URL from the task",
                "Navigate to the website",
                "Analyze the content of the page",
                "Provide a comprehensive summary"
            ]
            self.thinking.add_planning(plan)

            # Extract the URL
            self.thinking.add_thinking("Extracting URL...")
            prompt = f"I need to extract a URL from the following task:\n\n{task}\n\nPlease provide just the URL without any additional text."
            url = self.supervisor.get_response(prompt).strip()

            # Add execution step
            self.thinking.add_execution("extract_url", {
                "url": url
            })

            # Clean up the URL
            if not url.startswith("http"):
                url = "https://" + url
                self.thinking.add_thinking(f"Adding https:// prefix to URL: {url}")

            # Browse the website
            self.thinking.add_thinking(f"Browsing website: {url}")
            result = self.browser.browse(url)

            # Record the browsed URL
            self.thinking.add_link(
                url=result['url'],
                title=result.get('title', result['url']),
                description="Website that was browsed"
            )

            # Add execution step
            self.thinking.add_execution("browse", {
                "url": result['url'],
                "title": result.get('title', "")
            })

            # Add thinking step
            self.thinking.add_thinking("Analyzing the content and preparing a summary...")

            formatted_result = f"# Browsing Results\n\nURL: {result['url']}\nTitle: {result['title']}\n\n## Analysis\n\n{result['analysis']}"

        elif "extract" in task.lower() or "get information" in task.lower() or "find information" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be an information extraction task. I'll extract the URL and the specific information request.")

            # Create a plan
            plan = [
                "Extract the URL and information request from the task",
                "Navigate to the website",
                "Extract the requested information",
                "Provide the extracted information in a structured format"
            ]
            self.thinking.add_planning(plan)

            # Extract the URL and information request
            self.thinking.add_thinking("Extracting URL and information request...")
            prompt = f"I need to extract a URL and an information request from the following task:\n\n{task}\n\nPlease provide the URL and the information request in a structured format."
            extraction_info = self.supervisor.get_response(prompt)

            # Parse the extraction info
            lines = extraction_info.split("\n")
            url = ""
            information_request = ""

            for line in lines:
                if line.lower().startswith("url:"):
                    url = line.split(":", 1)[1].strip()
                elif line.lower().startswith("information request:") or line.lower().startswith("request:"):
                    information_request = line.split(":", 1)[1].strip()

            # Add execution step
            self.thinking.add_execution("extract_url_and_request", {
                "url": url,
                "information_request": information_request
            })

            # Clean up the URL
            if not url.startswith("http"):
                url = "https://" + url
                self.thinking.add_thinking(f"Adding https:// prefix to URL: {url}")

            # Extract information
            self.thinking.add_thinking(f"Browsing website {url} to extract information: '{information_request}'")
            result = self.browser.extract_information(url, information_request)

            # Record the browsed URL
            self.thinking.add_link(
                url=result['url'],
                title=result.get('title', result['url']),
                description=f"Website used for information extraction: {information_request}"
            )

            # Add execution step
            self.thinking.add_execution("extract_information", {
                "url": result['url'],
                "title": result.get('title', ""),
                "information_request": information_request
            })

            # Add thinking step
            self.thinking.add_thinking("Information extraction complete. Preparing the results...")

            formatted_result = f"# Information Extraction\n\nURL: {result['url']}\nTitle: {result['title']}\n\n## Extracted Information\n\n{result['extraction']}"

        else:
            # Add thinking step
            self.thinking.add_thinking("This appears to be a general web task. I'll default to search and browse.")

            # Create a plan
            plan = [
                "Use the task as a search query",
                "Perform a web search to find relevant pages",
                "Browse the top search result",
                "Analyze the content of the page",
                "Provide a comprehensive summary"
            ]
            self.thinking.add_planning(plan)

            # Default to search and browse
            self.thinking.add_thinking(f"Searching for: '{task}' and browsing the top result...")
            result = self.browser.search_and_browse(task)

            # Record the browsed URL
            self.thinking.add_link(
                url=result['browsed_url'],
                title=result.get('browse_result', {}).get('title', result['browsed_url']),
                description="Top search result that was browsed"
            )

            # Add execution step
            self.thinking.add_execution("search_and_browse", {
                "query": task,
                "url": result['browsed_url'],
                "title": result.get('browse_result', {}).get('title', "")
            })

            # Add thinking step
            self.thinking.add_thinking("Analyzing the content and preparing a summary...")

            formatted_result = f"# Search and Browse Results\n\nQuery: {task}\n\nURL: {result['browsed_url']}\n\n## Analysis\n\n{result['analysis']}"

        # Add the result to the task
        self.current_task["result"] = formatted_result
        self.current_task["end_time"] = time.time()
        self.tasks.append(self.current_task)

        return formatted_result

    def _process_supervisor_task(self, task: str) -> str:
        """
        Process a task with the supervisor agent.

        Args:
            task: Task to process

        Returns:
            Result of the task
        """
        # Record the task
        self.current_task = {
            "task": task,
            "specialist": "supervisor",
            "start_time": time.time(),
        }

        # Add thinking step
        self.thinking.add_thinking("This task requires general knowledge or coordination. I'll use the Supervisor agent to handle it directly.")

        # Create a plan
        plan = [
            "Analyze the user's request",
            "Determine the appropriate response",
            "Provide a comprehensive answer"
        ]
        self.thinking.add_planning(plan)

        # Get a response from the supervisor
        self.thinking.add_thinking("Generating response...")
        response = self.supervisor.get_response(task)

        # Add execution step
        self.thinking.add_execution("generate_response", {
            "response_length": len(response)
        })

        # Add thinking step
        self.thinking.add_thinking("Response generated successfully.")

        # Add the result to the task
        self.current_task["result"] = response
        self.current_task["end_time"] = time.time()
        self.tasks.append(self.current_task)

        return response

    def _extract_file_info(self, task: str) -> tuple:
        """
        Extract file path, content, and type from a task.

        Args:
            task: Task to extract from

        Returns:
            Tuple of (file_path, content, file_type)
        """
        # Ask the supervisor to extract the file information
        prompt = f"I need to extract file information from the following task:\n\n{task}\n\nPlease extract the following information:\n1. File path (where to save the file)\n2. Content to write to the file\n3. File type (markdown, python, etc.)\n\nProvide the information in a structured format."

        response = self.supervisor.get_response(prompt)

        # Parse the response
        file_path = None
        content = None
        file_type = None

        lines = response.split("\n")
        for line in lines:
            if line.lower().startswith("file path:") or line.lower().startswith("1. file path:"):
                file_path = line.split(":", 1)[1].strip()
            elif line.lower().startswith("content:") or line.lower().startswith("2. content:"):
                content_start = lines.index(line) + 1
                content_end = len(lines)

                for i in range(content_start, len(lines)):
                    if lines[i].lower().startswith("file type:") or lines[i].lower().startswith("3. file type:"):
                        content_end = i
                        break

                content = "\n".join(lines[content_start:content_end]).strip()
            elif line.lower().startswith("file type:") or line.lower().startswith("3. file type:"):
                file_type = line.split(":", 1)[1].strip()

        return file_path, content, file_type

    def _extract_file_path(self, task: str) -> Optional[str]:
        """
        Extract file path from a task.

        Args:
            task: Task to extract from

        Returns:
            File path or None if not found
        """
        # Ask the supervisor to extract the file path
        prompt = f"I need to extract the file path from the following task:\n\n{task}\n\nPlease extract the file path (the location of the file to read or operate on)."

        response = self.supervisor.get_response(prompt)

        # Parse the response
        lines = response.split("\n")
        for line in lines:
            if line.lower().startswith("file path:") or "file path" in line.lower():
                return line.split(":", 1)[1].strip()
            elif ":" not in line and "/" in line:
                return line.strip()

        return None

    def _extract_directory_path(self, task: str) -> Optional[str]:
        """
        Extract directory path from a task.

        Args:
            task: Task to extract from

        Returns:
            Directory path or None if not found
        """
        # Ask the supervisor to extract the directory path
        prompt = f"I need to extract the directory path from the following task:\n\n{task}\n\nPlease extract the directory path (the location of the directory to list or organize)."

        response = self.supervisor.get_response(prompt)

        # Parse the response
        lines = response.split("\n")
        for line in lines:
            if line.lower().startswith("directory path:") or "directory path" in line.lower():
                return line.split(":", 1)[1].strip()
            elif ":" not in line and "/" in line:
                return line.strip()

        return None

    def _extract_code(self, task: str) -> str:
        """
        Extract Python code from a task.

        Args:
            task: Task to extract code from

        Returns:
            Extracted code
        """
        # Use the supervisor to extract the code
        prompt = f"I need to extract Python code from the following task:\n\n{task}\n\nPlease extract only the Python code without any additional text. If there are multiple code blocks, combine them into a single coherent script. If there is no code, return an empty string."

        code = self.supervisor.get_response(prompt)

        # Clean up the code
        code = self._clean_code_block(code)

        return code

    def _extract_command(self, task: str) -> str:
        """
        Extract a shell command from a task.

        Args:
            task: Task to extract command from

        Returns:
            Extracted command
        """
        # Use the supervisor to extract the command
        prompt = f"I need to extract a shell command from the following task:\n\n{task}\n\nPlease extract only the shell command without any additional text. If there are multiple commands, combine them into a single command line (using && if needed). If there is no command, return an empty string."

        command = self.supervisor.get_response(prompt)

        # Clean up the command
        command = self._clean_code_block(command)

        return command

    def _clean_code_block(self, text: str) -> str:
        """
        Clean up a code block by removing markdown formatting.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        # Remove markdown code block markers
        lines = text.split("\n")
        cleaned_lines = []
        in_code_block = False

        for line in lines:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            if not in_code_block or line.strip():
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()

    def _process_sandbox_task(self, task: str) -> str:
        """
        Process a task with the sandbox agent.

        Args:
            task: Task to process

        Returns:
            Result of the task
        """
        # Record the task
        self.current_task = {
            "task": task,
            "specialist": "sandbox",
            "start_time": time.time(),
        }

        # Add thinking step
        self.thinking.add_thinking("I'll use the Sandbox agent to execute code or commands in a safe environment.")

        # Determine the type of sandbox task
        if "list directory" in task.lower() or "list files" in task.lower() or "show directory" in task.lower() or "show files" in task.lower():
            return self._handle_list_directory(task)
        elif "create directory" in task.lower() or "make directory" in task.lower() or "make folder" in task.lower() or "create folder" in task.lower():
            return self._handle_create_directory(task)
        elif "copy file" in task.lower() or "duplicate file" in task.lower():
            return self._handle_copy_file(task)
        elif "move file" in task.lower() or "rename file" in task.lower():
            return self._handle_move_file(task)
        elif "find files" in task.lower() or "search files" in task.lower() or "find file" in task.lower() or "search file" in task.lower():
            return self._handle_find_files(task)
        elif "file info" in task.lower() or "file information" in task.lower() or "file details" in task.lower() or "file stats" in task.lower():
            return self._handle_file_info(task)
        elif "create file" in task.lower() or "write file" in task.lower() or "save file" in task.lower() or "make file" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be a file creation task. I'll extract the file information.")

            # Create a plan
            plan = [
                "Extract the filename and content from the task",
                "Create the file in the sandbox environment",
                "Verify the file was created successfully",
                "Provide a confirmation and summary"
            ]
            self.thinking.add_planning(plan)

            # Extract file information
            self.thinking.add_thinking("Extracting file information...")
            file_info = self.sandbox.extract_file_info(task)

            # Add execution step
            self.thinking.add_execution("extract_file_info", {
                "filename": file_info.get("filename", "Not found"),
                "content_length": len(file_info.get("content", "")) if file_info.get("content") else 0
            })

            if file_info.get("filename") and file_info.get("content"):
                # Add thinking step
                self.thinking.add_thinking(f"Creating file '{file_info['filename']}' with {len(file_info['content'])} characters of content.")

                # Create the file
                result = self.sandbox.create_file(file_info["filename"], file_info["content"])

                # Add execution step
                self.thinking.add_execution("create_file", {
                    "status": result["status"],
                    "filename": result.get("filename", ""),
                    "file_path": result.get("file_path", "")
                })

                # Add file to thinking process
                self.thinking.add_file(
                    path=result.get("filename", ""),
                    content=file_info["content"][:500] + ('...' if len(file_info["content"]) > 500 else ''),
                    description=f"File created with {len(file_info['content'])} characters of content"
                )

                # Format the result
                if result["status"] == "success":
                    # Add thinking step
                    self.thinking.add_thinking(f"File created successfully at {result.get('file_path', '')}.")

                    formatted_result = f"# File Created\n\nFile: {result.get('filename', '')}\n\n## Content\n\n```\n{file_info['content'][:500]}{'...' if len(file_info['content']) > 500 else ''}\n```\n\n## Status\n\nFile was successfully created in the sandbox environment."
                else:
                    # Add thinking step
                    self.thinking.add_thinking(f"Failed to create file: {result.get('error', '')}")

                    formatted_result = f"# File Creation Failed\n\nFile: {file_info.get('filename', '')}\n\n## Error\n\n{result.get('error', '')}\n\nPlease check the filename and try again."
            else:
                # Add thinking step
                self.thinking.add_thinking("I couldn't extract the filename or content from the request.")

                formatted_result = "I couldn't extract the necessary information to create a file. Please provide both a filename and content in your request."

        elif "python" in task.lower() or "code" in task.lower() or "script" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be a code execution task. I'll extract the Python code to execute.")

            # Create a plan
            plan = [
                "Extract the Python code from the task",
                "Prepare the code for execution",
                "Execute the code in a sandbox environment",
                "Analyze the execution results",
                "Provide a comprehensive summary"
            ]
            self.thinking.add_planning(plan)

            # Extract the code
            self.thinking.add_thinking("Extracting Python code...")
            code = self._extract_code(task)

            # Add execution step
            self.thinking.add_execution("extract_code", {
                "code_length": len(code) if code else 0
            })

            if code:
                # Add thinking step
                self.thinking.add_thinking(f"Executing the following Python code:\n\n```python\n{code}\n```")

                # Add file to thinking process
                code_filename = "sandbox_code.py"
                self.thinking.add_file(
                    path=code_filename,
                    content=code,
                    description="Python code to execute in sandbox"
                )

                # Execute the code
                result = self.sandbox.execute_python(code)

                # Add execution step
                self.thinking.add_execution("execute_python", {
                    "status": result["status"],
                    "stdout_length": len(result.get("stdout", "")),
                    "stderr_length": len(result.get("stderr", ""))
                })

                # Format the result
                formatted_result = f"# Code Execution Result\n\n## Code\n\n```python\n{code}\n```\n\n## Output\n\n"

                if result["status"] == "success":
                    # Add thinking step
                    self.thinking.add_thinking("Code executed successfully!")

                    if result.get("stdout"):
                        self.thinking.add_thinking(f"Output:\n\n```\n{result['stdout']}\n```")
                        formatted_result += f"```\n{result['stdout']}\n```\n\n"
                    else:
                        formatted_result += "No output produced.\n\n"
                else:
                    # Add thinking step
                    self.thinking.add_thinking(f"Code execution failed with error:\n\n```\n{result.get('stderr', '')}\n```")

                    formatted_result += f"Error:\n```\n{result.get('stderr', '')}\n```\n\n"

                # Add analysis
                formatted_result += f"## Analysis\n\n{result.get('analysis', '')}"
            else:
                # Add thinking step
                self.thinking.add_thinking("I couldn't extract any Python code from the request.")

                formatted_result = "I couldn't extract any Python code from your request. Please provide the code you want to execute."

        elif "command" in task.lower() or "shell" in task.lower() or "terminal" in task.lower() or "bash" in task.lower() or "run" in task.lower():
            # Add thinking step
            self.thinking.add_thinking("This appears to be a command execution task. I'll extract the shell command to execute.")

            # Create a plan
            plan = [
                "Extract the shell command from the task",
                "Prepare the command for execution",
                "Execute the command in a sandbox environment",
                "Analyze the execution results",
                "Provide a comprehensive summary"
            ]
            self.thinking.add_planning(plan)

            # Extract the command
            self.thinking.add_thinking("Extracting shell command...")
            command = self._extract_command(task)

            # Add execution step
            self.thinking.add_execution("extract_command", {
                "command": command
            })

            if command:
                # Add thinking step
                self.thinking.add_thinking(f"Executing the following shell command:\n\n```bash\n{command}\n```")

                # Execute the command
                result = self.sandbox.execute_command(command)

                # Add execution step
                self.thinking.add_execution("execute_command", {
                    "status": result["status"],
                    "stdout_length": len(result.get("stdout", "")),
                    "stderr_length": len(result.get("stderr", ""))
                })

                # Format the result
                formatted_result = f"# Command Execution Result\n\n## Command\n\n```bash\n{command}\n```\n\n## Output\n\n"

                if result["status"] == "success":
                    # Add thinking step
                    self.thinking.add_thinking("Command executed successfully!")

                    if result.get("stdout"):
                        self.thinking.add_thinking(f"Output:\n\n```\n{result['stdout']}\n```")
                        formatted_result += f"```\n{result['stdout']}\n```\n\n"
                    else:
                        formatted_result += "No output produced.\n\n"
                else:
                    # Add thinking step
                    self.thinking.add_thinking(f"Command execution failed with error:\n\n```\n{result.get('stderr', '')}\n```")

                    formatted_result += f"Error:\n```\n{result.get('stderr', '')}\n```\n\n"

                # Add analysis
                formatted_result += f"## Analysis\n\n{result.get('analysis', '')}"
            else:
                # Add thinking step
                self.thinking.add_thinking("I couldn't extract any shell command from the request.")

                formatted_result = "I couldn't extract any shell command from your request. Please provide the command you want to execute."

        else:
            # Add thinking step
            self.thinking.add_thinking("I'm not sure what type of sandbox task is being requested. I'll ask the user for clarification.")

            formatted_result = "I'm not sure if you want me to execute Python code or a shell command. Please specify which type of execution you need and provide the code or command."

        # Add the result to the task
        self.current_task["result"] = formatted_result
        self.current_task["end_time"] = time.time()
        self.tasks.append(self.current_task)

        return formatted_result

    def _handle_list_directory(self, task: str) -> str:
        """
        Handle a directory listing task.

        Args:
            task: The task description

        Returns:
            Formatted result
        """
        # Add thinking step
        self.thinking.add_thinking("This appears to be a directory listing task. I'll extract the directory path.")

        # Create a plan
        plan = [
            "Extract the directory path from the task",
            "List the directory contents",
            "Analyze the directory structure",
            "Provide a comprehensive summary"
        ]
        self.thinking.add_planning(plan)

        # Extract the directory path
        self.thinking.add_thinking("Extracting directory path...")
        directory = self._extract_path(task) or ""

        # Add execution step
        self.thinking.add_execution("extract_path", {
            "path": directory
        })

        # Add thinking step
        self.thinking.add_thinking(f"Listing contents of directory '{directory}'...")

        # List the directory
        result = self.sandbox.list_directory(directory)

        # Add execution step
        self.thinking.add_execution("list_directory", {
            "path": directory,
            "status": result["status"],
            "item_count": len(result.get("items", [])) if result["status"] == "success" else 0
        })

        # Format the result
        if result["status"] == "success":
            # Add thinking step
            self.thinking.add_thinking(f"Successfully listed directory '{directory}'.")

            items = result.get("items", [])

            formatted_result = f"# Directory Contents\n\nPath: {directory or '.'}\n\n## Items\n\n"

            if not items:
                formatted_result += "Directory is empty.\n"
            else:
                for item in items:
                    item_type = "Directory" if item.get("is_dir", False) else "File"
                    size = item.get("size", 0)
                    formatted_result += f"- {item.get('name', '')}: {item_type}, {size} bytes\n"

            formatted_result += f"\n## Analysis\n\n{result.get('analysis', '')}"
        else:
            # Add thinking step
            self.thinking.add_thinking(f"Error listing directory: {result.get('error', '')}")

            formatted_result = f"# Error Listing Directory\n\nPath: {directory or '.'}\n\n## Error\n\n{result.get('error', '')}"

        return formatted_result

    def _handle_create_directory(self, task: str) -> str:
        """
        Handle a directory creation task.

        Args:
            task: The task description

        Returns:
            Formatted result
        """
        # Add thinking step
        self.thinking.add_thinking("This appears to be a directory creation task. I'll extract the directory path.")

        # Create a plan
        plan = [
            "Extract the directory path from the task",
            "Create the directory",
            "Verify the directory was created successfully",
            "Provide a confirmation and summary"
        ]
        self.thinking.add_planning(plan)

        # Extract the directory path
        self.thinking.add_thinking("Extracting directory path...")
        directory = self._extract_path(task)

        # Add execution step
        self.thinking.add_execution("extract_path", {
            "path": directory
        })

        if not directory:
            # Add thinking step
            self.thinking.add_thinking("I couldn't extract a directory path from the request.")

            return "I couldn't extract a directory path from your request. Please provide a specific path for the directory you want to create."

        # Add thinking step
        self.thinking.add_thinking(f"Creating directory '{directory}'...")

        # Create the directory
        result = self.sandbox.create_directory(directory)

        # Add execution step
        self.thinking.add_execution("create_directory", {
            "path": directory,
            "status": result["status"]
        })

        # Format the result
        if result["status"] == "success":
            # Add thinking step
            self.thinking.add_thinking(f"Successfully created directory '{directory}'.")

            formatted_result = f"# Directory Created\n\nPath: {directory}\n\n## Status\n\n{result.get('message', 'Directory created successfully.')}"
        else:
            # Add thinking step
            self.thinking.add_thinking(f"Error creating directory: {result.get('error', '')}")

            formatted_result = f"# Error Creating Directory\n\nPath: {directory}\n\n## Error\n\n{result.get('error', '')}"

        return formatted_result

    def _handle_copy_file(self, task: str) -> str:
        """
        Handle a file copy task.

        Args:
            task: The task description

        Returns:
            Formatted result
        """
        # Add thinking step
        self.thinking.add_thinking("This appears to be a file copy task. I'll extract the source and destination paths.")

        # Create a plan
        plan = [
            "Extract the source and destination paths from the task",
            "Copy the file",
            "Verify the file was copied successfully",
            "Provide a confirmation and summary"
        ]
        self.thinking.add_planning(plan)

        # Extract the source and destination paths
        self.thinking.add_thinking("Extracting source and destination paths...")
        source, destination = self._extract_source_destination(task)

        # Add execution step
        self.thinking.add_execution("extract_paths", {
            "source": source,
            "destination": destination
        })

        if not source or not destination:
            # Add thinking step
            self.thinking.add_thinking("I couldn't extract both source and destination paths from the request.")

            return "I couldn't extract both source and destination paths from your request. Please provide specific paths for the file you want to copy and where you want to copy it to."

        # Add thinking step
        self.thinking.add_thinking(f"Copying file from '{source}' to '{destination}'...")

        # Copy the file
        result = self.sandbox.copy_file(source, destination)

        # Add execution step
        self.thinking.add_execution("copy_file", {
            "source": source,
            "destination": destination,
            "status": result["status"]
        })

        # Format the result
        if result["status"] == "success":
            # Add thinking step
            self.thinking.add_thinking(f"Successfully copied file from '{source}' to '{destination}'.")

            formatted_result = f"# File Copied\n\nSource: {source}\nDestination: {destination}\n\n## Status\n\n{result.get('message', 'File copied successfully.')}"
        else:
            # Add thinking step
            self.thinking.add_thinking(f"Error copying file: {result.get('error', '')}")

            formatted_result = f"# Error Copying File\n\nSource: {source}\nDestination: {destination}\n\n## Error\n\n{result.get('error', '')}"

        return formatted_result

    def _handle_move_file(self, task: str) -> str:
        """
        Handle a file move task.

        Args:
            task: The task description

        Returns:
            Formatted result
        """
        # Add thinking step
        self.thinking.add_thinking("This appears to be a file move task. I'll extract the source and destination paths.")

        # Create a plan
        plan = [
            "Extract the source and destination paths from the task",
            "Move the file",
            "Verify the file was moved successfully",
            "Provide a confirmation and summary"
        ]
        self.thinking.add_planning(plan)

        # Extract the source and destination paths
        self.thinking.add_thinking("Extracting source and destination paths...")
        source, destination = self._extract_source_destination(task)

        # Add execution step
        self.thinking.add_execution("extract_paths", {
            "source": source,
            "destination": destination
        })

        if not source or not destination:
            # Add thinking step
            self.thinking.add_thinking("I couldn't extract both source and destination paths from the request.")

            return "I couldn't extract both source and destination paths from your request. Please provide specific paths for the file you want to move and where you want to move it to."

        # Add thinking step
        self.thinking.add_thinking(f"Moving file from '{source}' to '{destination}'...")

        # Move the file
        result = self.sandbox.move_file(source, destination)

        # Add execution step
        self.thinking.add_execution("move_file", {
            "source": source,
            "destination": destination,
            "status": result["status"]
        })

        # Format the result
        if result["status"] == "success":
            # Add thinking step
            self.thinking.add_thinking(f"Successfully moved file from '{source}' to '{destination}'.")

            formatted_result = f"# File Moved\n\nSource: {source}\nDestination: {destination}\n\n## Status\n\n{result.get('message', 'File moved successfully.')}"
        else:
            # Add thinking step
            self.thinking.add_thinking(f"Error moving file: {result.get('error', '')}")

            formatted_result = f"# Error Moving File\n\nSource: {source}\nDestination: {destination}\n\n## Error\n\n{result.get('error', '')}"

        return formatted_result

    def _handle_find_files(self, task: str) -> str:
        """
        Handle a file search task.

        Args:
            task: The task description

        Returns:
            Formatted result
        """
        # Add thinking step
        self.thinking.add_thinking("This appears to be a file search task. I'll extract the search pattern.")

        # Create a plan
        plan = [
            "Extract the search pattern from the task",
            "Find files matching the pattern",
            "Analyze the search results",
            "Provide a comprehensive summary"
        ]
        self.thinking.add_planning(plan)

        # Extract the search pattern
        self.thinking.add_thinking("Extracting search pattern...")
        pattern = self._extract_pattern(task)

        # Add execution step
        self.thinking.add_execution("extract_pattern", {
            "pattern": pattern
        })

        if not pattern:
            # Add thinking step
            self.thinking.add_thinking("I couldn't extract a search pattern from the request.")

            return "I couldn't extract a search pattern from your request. Please provide a specific pattern for the files you want to find."

        # Add thinking step
        self.thinking.add_thinking(f"Finding files matching pattern '{pattern}'...")

        # Find the files
        result = self.sandbox.find_files(pattern)

        # Add execution step
        self.thinking.add_execution("find_files", {
            "pattern": pattern,
            "status": result["status"],
            "match_count": result.get("count", 0) if result["status"] == "success" else 0
        })

        # Format the result
        if result["status"] == "success":
            # Add thinking step
            self.thinking.add_thinking(f"Found {result.get('count', 0)} files matching pattern '{pattern}'.")

            matches = result.get("matches", [])

            formatted_result = f"# Search Results\n\nPattern: {pattern}\n\n## Matches ({len(matches)})\n\n"

            if not matches:
                formatted_result += "No files found matching the pattern.\n"
            else:
                for match in matches:
                    item_type = "Directory" if match.get("is_dir", False) else "File"
                    size = match.get("size", 0)
                    formatted_result += f"- {match.get('path', '')}: {item_type}, {size} bytes\n"

            formatted_result += f"\n## Analysis\n\n{result.get('analysis', '')}"
        else:
            # Add thinking step
            self.thinking.add_thinking(f"Error finding files: {result.get('error', '')}")

            formatted_result = f"# Error Finding Files\n\nPattern: {pattern}\n\n## Error\n\n{result.get('error', '')}"

        return formatted_result

    def _handle_file_info(self, task: str) -> str:
        """
        Handle a file info task.

        Args:
            task: The task description

        Returns:
            Formatted result
        """
        # Add thinking step
        self.thinking.add_thinking("This appears to be a file info task. I'll extract the file path.")

        # Create a plan
        plan = [
            "Extract the file path from the task",
            "Get information about the file",
            "Analyze the file information",
            "Provide a comprehensive summary"
        ]
        self.thinking.add_planning(plan)

        # Extract the file path
        self.thinking.add_thinking("Extracting file path...")
        path = self._extract_path(task)

        # Add execution step
        self.thinking.add_execution("extract_path", {
            "path": path
        })

        if not path:
            # Add thinking step
            self.thinking.add_thinking("I couldn't extract a file path from the request.")

            return "I couldn't extract a file path from your request. Please provide a specific path for the file you want information about."

        # Add thinking step
        self.thinking.add_thinking(f"Getting information about '{path}'...")

        # Get the file info
        result = self.sandbox.get_file_info(path)

        # Add execution step
        self.thinking.add_execution("get_file_info", {
            "path": path,
            "status": result["status"]
        })

        # Format the result
        if result["status"] == "success":
            # Add thinking step
            self.thinking.add_thinking(f"Successfully retrieved information about '{path}'.")

            formatted_result = f"# File Information\n\nPath: {path}\n\n## Details\n\n"

            if result.get("is_dir", False):
                formatted_result += "Type: Directory\n"
            else:
                formatted_result += f"Type: File\nSize: {result.get('size', 0)} bytes\n"

            formatted_result += f"Created: {time.ctime(result.get('created', 0))}\n"
            formatted_result += f"Modified: {time.ctime(result.get('modified', 0))}\n"
            formatted_result += f"Accessed: {time.ctime(result.get('accessed', 0))}\n"

            formatted_result += f"\n## Analysis\n\n{result.get('analysis', '')}"
        else:
            # Add thinking step
            self.thinking.add_thinking(f"Error getting file information: {result.get('error', '')}")

            formatted_result = f"# Error Getting File Information\n\nPath: {path}\n\n## Error\n\n{result.get('error', '')}"

        return formatted_result

    def _extract_path(self, task: str) -> str:
        """
        Extract a file or directory path from a task.

        Args:
            task: The task description

        Returns:
            The extracted path
        """
        # Use the supervisor to extract the path
        prompt = f"I need to extract a file or directory path from the following task:\n\n{task}\n\nPlease extract only the path without any additional text. If there is no path, return an empty string."

        path = self.supervisor.get_response(prompt).strip()

        # Clean up the path
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        elif path.startswith("'") and path.endswith("'"):
            path = path[1:-1]

        return path

    def _extract_source_destination(self, task: str) -> tuple:
        """
        Extract source and destination paths from a task.

        Args:
            task: The task description

        Returns:
            A tuple of (source, destination)
        """
        # Use the supervisor to extract the paths
        prompt = f"I need to extract source and destination paths from the following task:\n\n{task}\n\nPlease extract only the paths without any additional text. Return them in the format:\n\nSource: <source_path>\nDestination: <destination_path>\n\nIf either path is missing, use 'Not found' for that path."

        response = self.supervisor.get_response(prompt)

        # Parse the response
        source = None
        destination = None

        for line in response.split("\n"):
            if line.lower().startswith("source:"):
                source = line.split(":", 1)[1].strip()
                if source.lower() == "not found":
                    source = None
            elif line.lower().startswith("destination:"):
                destination = line.split(":", 1)[1].strip()
                if destination.lower() == "not found":
                    destination = None

        # Clean up the paths
        if source and source.startswith('"') and source.endswith('"'):
            source = source[1:-1]
        elif source and source.startswith("'") and source.endswith("'"):
            source = source[1:-1]

        if destination and destination.startswith('"') and destination.endswith('"'):
            destination = destination[1:-1]
        elif destination and destination.startswith("'") and destination.endswith("'"):
            destination = destination[1:-1]

        return source, destination

    def _extract_pattern(self, task: str) -> str:
        """
        Extract a search pattern from a task.

        Args:
            task: The task description

        Returns:
            The extracted pattern
        """
        # Use the supervisor to extract the pattern
        prompt = f"I need to extract a file search pattern from the following task:\n\n{task}\n\nPlease extract only the pattern without any additional text. If there is no pattern, return an empty string."

        pattern = self.supervisor.get_response(prompt).strip()

        # Clean up the pattern
        if pattern.startswith('"') and pattern.endswith('"'):
            pattern = pattern[1:-1]
        elif pattern.startswith("'") and pattern.endswith("'"):
            pattern = pattern[1:-1]

        return pattern

def run_agent_workflow(user_input: str, debug: bool = False, use_enhanced_browser: bool = True, thinking_mode: str = ThinkingProcess.NORMAL_THINKING) -> Dict[str, Any]:
    """
    Run the agent workflow.

    Args:
        user_input: User input to process
        debug: Whether to enable debug mode
        use_enhanced_browser: Whether to use the enhanced SuperNova browser
        thinking_mode: The level of detail in thinking process (normal, deep, super_deep)

    Returns:
        A dictionary containing the workflow result
    """
    workflow = AgentWorkflow(debug=debug, use_enhanced_browser=use_enhanced_browser, thinking_mode=thinking_mode)
    return workflow.run(user_input)

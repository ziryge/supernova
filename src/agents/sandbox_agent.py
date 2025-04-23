"""
Sandbox agent for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAgent
from ..tools.sandbox import sandbox

class SandboxAgent(BaseAgent):
    """Agent that provides a sandbox environment for code execution and commands."""

    def __init__(self):
        """Initialize the sandbox agent."""
        super().__init__("sandbox", use_reasoning_llm=True)

    def execute_python(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in a sandbox environment.

        Args:
            code: Python code to execute

        Returns:
            A dictionary containing the execution result
        """
        # Execute the code
        result = sandbox.execute_python(code)

        # Analyze the result
        if result["status"] == "success":
            analysis = self._analyze_success(result["stdout"], code)
        else:
            analysis = self._analyze_error(result["stderr"], code)

        return {
            "status": result["status"],
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "file_id": result.get("file_id", ""),
            "file_path": result.get("file_path", ""),
            "analysis": analysis,
            "code": code
        }

    def execute_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a shell command in a sandbox environment.

        Args:
            command: Shell command to execute

        Returns:
            A dictionary containing the execution result
        """
        # Execute the command
        result = sandbox.execute_command(command)

        # Analyze the result
        if result["status"] == "success":
            analysis = self._analyze_command_success(result["stdout"], command)
        else:
            analysis = self._analyze_command_error(result["stderr"], command)

        return {
            "status": result["status"],
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "command": command,
            "analysis": analysis
        }

    def create_file(self, filename: str, content: str) -> Dict[str, Any]:
        """
        Create a file in the sandbox environment.

        Args:
            filename: Name of the file to create
            content: Content of the file

        Returns:
            A dictionary containing the result
        """
        # Create the file
        result = sandbox.create_file(filename, content)

        return {
            "status": result["status"],
            "file_id": result.get("file_id", ""),
            "file_path": result.get("file_path", ""),
            "filename": filename,
            "content": content,
            "error": result.get("error", "")
        }

    def read_file(self, filename: str) -> Dict[str, Any]:
        """
        Read a file from the sandbox environment.

        Args:
            filename: Name of the file to read

        Returns:
            A dictionary containing the file content
        """
        # Read the file
        result = sandbox.read_file(filename)

        return {
            "status": result["status"],
            "content": result.get("content", ""),
            "file_path": result.get("file_path", ""),
            "filename": filename,
            "error": result.get("error", "")
        }

    def list_files(self) -> Dict[str, Any]:
        """
        List all files in the sandbox environment.

        Returns:
            A dictionary containing the list of files
        """
        # List the files
        result = sandbox.list_files()

        return {
            "status": result["status"],
            "files": result.get("files", []),
            "error": result.get("error", "")
        }

    def delete_file(self, filename: str) -> Dict[str, Any]:
        """
        Delete a file from the sandbox environment.

        Args:
            filename: Name of the file to delete

        Returns:
            A dictionary containing the result
        """
        # Delete the file
        result = sandbox.delete_file(filename)

        return {
            "status": result["status"],
            "filename": filename,
            "error": result.get("error", "")
        }

    def clean(self) -> Dict[str, Any]:
        """
        Clean the sandbox environment by removing all files.

        Returns:
            A dictionary containing the result
        """
        # Clean the sandbox
        result = sandbox.clean()

        return {
            "status": result["status"],
            "message": result.get("message", ""),
            "error": result.get("error", "")
        }

    def _analyze_success(self, stdout: str, code: str) -> str:
        """
        Analyze successful code execution.

        Args:
            stdout: Standard output from the execution
            code: The executed code

        Returns:
            Analysis of the execution
        """
        prompt = f"""
        I executed the following Python code:

        ```python
        {code}
        ```

        The code executed successfully with the following output:

        ```
        {stdout}
        ```

        Please analyze the execution and provide a summary of what the code did and what the output means.
        """

        return self.get_response(prompt)

    def _analyze_error(self, stderr: str, code: str) -> str:
        """
        Analyze failed code execution.

        Args:
            stderr: Standard error from the execution
            code: The executed code

        Returns:
            Analysis of the error
        """
        prompt = f"""
        I tried to execute the following Python code:

        ```python
        {code}
        ```

        The code failed with the following error:

        ```
        {stderr}
        ```

        Please analyze the error and provide a detailed explanation of what went wrong and how to fix it.
        """

        return self.get_response(prompt)

    def _analyze_command_success(self, stdout: str, command: str) -> str:
        """
        Analyze successful command execution.

        Args:
            stdout: Standard output from the execution
            command: The executed command

        Returns:
            Analysis of the execution
        """
        prompt = f"""
        I executed the following shell command:

        ```
        {command}
        ```

        The command executed successfully with the following output:

        ```
        {stdout}
        ```

        Please analyze the execution and provide a summary of what the command did and what the output means.
        """

        return self.get_response(prompt)

    def _analyze_command_error(self, stderr: str, command: str) -> str:
        """
        Analyze failed command execution.

        Args:
            stderr: Standard error from the execution
            command: The executed command

        Returns:
            Analysis of the error
        """
        prompt = f"""
        I tried to execute the following shell command:

        ```
        {command}
        ```

        The command failed with the following error:

        ```
        {stderr}
        ```

        Please analyze the error and provide a detailed explanation of what went wrong and how to fix it.
        """

        return self.get_response(prompt)

    def _analyze_directory_listing(self, result: Dict[str, Any]) -> str:
        """
        Analyze a directory listing result.

        Args:
            result: Directory listing result

        Returns:
            Analysis of the directory listing
        """
        path = result.get("path", "")
        items = result.get("items", [])

        if not items:
            return f"Directory '{path}' is empty."

        # Count files and directories
        file_count = sum(1 for item in items if not item.get("is_dir", False))
        dir_count = sum(1 for item in items if item.get("is_dir", False))

        analysis = f"Directory '{path}' contains {len(items)} items: {file_count} files and {dir_count} directories."

        return analysis

    def extract_file_info(self, request: str) -> Dict[str, Any]:
        """
        Extract file information from a user request.

        Args:
            request: User request containing file information

        Returns:
            A dictionary containing the extracted file information
        """
        prompt = f"""
        I need to extract file information from the following request:

        ```
        {request}
        ```

        Please extract the following information:
        1. The filename or file path
        2. The file content

        Return the information in the following format:

        Filename: <extracted filename>
        Content: <extracted content>

        If you cannot extract the filename or content, indicate that with "Not found".
        """

        response = self.get_response(prompt)

        # Parse the response
        filename = None
        content = None

        for line in response.split("\n"):
            if line.lower().startswith("filename:"):
                filename = line.split(":", 1)[1].strip()
                if filename.lower() == "not found":
                    filename = None
            elif line.lower().startswith("content:"):
                content_start = line.find(":", 1) + 1
                content = line[content_start:].strip()
                if content.lower() == "not found":
                    content = None

        # If content spans multiple lines, extract it
        if content is None or content == "":
            content_start = response.find("Content:") + 8
            if content_start > 8:
                content = response[content_start:].strip()
                if content.lower() == "not found":
                    content = None

        return {
            "filename": filename,
            "content": content
        }

    def create_file_from_request(self, request: str) -> Dict[str, Any]:
        """
        Create a file based on a user request.

        Args:
            request: User request containing file information

        Returns:
            A dictionary containing the result
        """
        # Extract file information
        file_info = self.extract_file_info(request)

        if not file_info["filename"]:
            return {
                "status": "error",
                "error": "Could not extract filename from request",
                "request": request
            }

        if not file_info["content"]:
            return {
                "status": "error",
                "error": "Could not extract content from request",
                "request": request
            }

        # Create the file
        result = self.create_file(file_info["filename"], file_info["content"])

        # Add analysis
        if result["status"] == "success":
            analysis = f"Successfully created file '{file_info['filename']}' with {len(file_info['content'])} characters of content."
        else:
            analysis = f"Failed to create file '{file_info['filename']}': {result['error']}"

        result["analysis"] = analysis

        return result

    def list_directory(self, path: str = "") -> Dict[str, Any]:
        """
        List contents of a directory in the sandbox.

        Args:
            path: Relative path within the sandbox

        Returns:
            Dictionary with directory contents
        """
        result = sandbox.list_directory(path)

        # Add analysis
        if result["status"] == "success":
            analysis = self._analyze_directory_listing(result)
        else:
            analysis = f"Error listing directory: {result.get('error', 'Unknown error')}"

        result["analysis"] = analysis
        return result

    def create_directory(self, path: str) -> Dict[str, Any]:
        """
        Create a directory in the sandbox.

        Args:
            path: Relative path within the sandbox

        Returns:
            Dictionary with operation result
        """
        result = sandbox.create_directory(path)

        # Add analysis
        if result["status"] == "success":
            analysis = f"Successfully created directory '{path}'."
        else:
            analysis = f"Failed to create directory '{path}': {result.get('error', 'Unknown error')}"

        result["analysis"] = analysis
        return result

    def copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """
        Copy a file within the sandbox.

        Args:
            source: Source path relative to sandbox
            destination: Destination path relative to sandbox

        Returns:
            Dictionary with operation result
        """
        result = sandbox.copy_file(source, destination)

        # Add analysis
        if result["status"] == "success":
            analysis = f"Successfully copied file from '{source}' to '{destination}'."
        else:
            analysis = f"Failed to copy file from '{source}' to '{destination}': {result.get('error', 'Unknown error')}"

        result["analysis"] = analysis
        return result

    def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """
        Move a file within the sandbox.

        Args:
            source: Source path relative to sandbox
            destination: Destination path relative to sandbox

        Returns:
            Dictionary with operation result
        """
        result = sandbox.move_file(source, destination)

        # Add analysis
        if result["status"] == "success":
            analysis = f"Successfully moved file from '{source}' to '{destination}'."
        else:
            analysis = f"Failed to move file from '{source}' to '{destination}': {result.get('error', 'Unknown error')}"

        result["analysis"] = analysis
        return result

    def find_files(self, pattern: str) -> Dict[str, Any]:
        """
        Find files matching a pattern in the sandbox.

        Args:
            pattern: Glob pattern to match files

        Returns:
            Dictionary with matching files
        """
        result = sandbox.find_files(pattern)

        # Add analysis
        if result["status"] == "success":
            if result["count"] > 0:
                analysis = f"Found {result['count']} files matching pattern '{pattern}'."
            else:
                analysis = f"No files found matching pattern '{pattern}'."
        else:
            analysis = f"Error finding files with pattern '{pattern}': {result.get('error', 'Unknown error')}"

        result["analysis"] = analysis
        return result

    def get_file_info(self, path: str) -> Dict[str, Any]:
        """
        Get information about a file in the sandbox.

        Args:
            path: Relative path within the sandbox

        Returns:
            Dictionary with file information
        """
        result = sandbox.get_file_info(path)

        # Add analysis
        if result["status"] == "success":
            if result["is_dir"]:
                analysis = f"'{path}' is a directory."
            else:
                analysis = f"'{path}' is a file of size {result['size']} bytes."
        else:
            analysis = f"Error getting information for '{path}': {result.get('error', 'Unknown error')}"

        result["analysis"] = analysis
        return result

"""
Sandbox environment for SuperNova AI to safely execute code and commands.
"""

import os
import sys
import subprocess
import tempfile
import uuid
import time
from typing import Dict, Any, List, Optional, Union
import traceback

from ..config.env import ToolConfig, DEBUG
from .sandbox_fs import SandboxFileSystem

class Sandbox:
    """Sandbox environment for executing code and commands."""

    def __init__(self):
        """Initialize the sandbox environment."""
        self.workspace_dir = os.path.join(tempfile.gettempdir(), "supernova_sandbox")
        os.makedirs(self.workspace_dir, exist_ok=True)

        # Track created files
        self.files = {}

        # Initialize file system
        self.fs = SandboxFileSystem(self.workspace_dir)

        if DEBUG:
            print(f"Sandbox initialized at {self.workspace_dir}")

    def execute_python(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in a sandbox environment.

        Args:
            code: Python code to execute

        Returns:
            A dictionary containing the execution result
        """
        # Create a temporary file for the code
        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.workspace_dir, f"{file_id}.py")

        try:
            # Write the code to the file
            with open(file_path, "w") as f:
                f.write(code)

            # Track the file
            self.files[file_id] = {
                "path": file_path,
                "type": "python",
                "content": code,
                "created_at": time.time()
            }

            # Execute the code in a subprocess
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )

            # Process the result
            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "file_id": file_id,
                "file_path": file_path
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "Execution timed out after 30 seconds",
                "file_id": file_id,
                "file_path": file_path
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "file_id": file_id,
                "file_path": file_path
            }

    def execute_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a shell command in a sandbox environment.

        Args:
            command: Shell command to execute

        Returns:
            A dictionary containing the execution result
        """
        try:
            # Execute the command in a subprocess
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                cwd=self.workspace_dir
            )

            # Process the result
            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "Execution timed out after 30 seconds",
                "command": command
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "command": command
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
        try:
            # Create a file in the sandbox
            file_path = os.path.join(self.workspace_dir, filename)

            # Create directories if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the content to the file
            with open(file_path, "w") as f:
                f.write(content)

            # Track the file
            file_id = str(uuid.uuid4())
            self.files[file_id] = {
                "path": file_path,
                "type": "file",
                "content": content,
                "created_at": time.time()
            }

            return {
                "status": "success",
                "file_id": file_id,
                "file_path": file_path,
                "filename": filename
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "filename": filename
            }

    def read_file(self, filename: str) -> Dict[str, Any]:
        """
        Read a file from the sandbox environment.

        Args:
            filename: Name of the file to read

        Returns:
            A dictionary containing the file content
        """
        try:
            # Read a file from the sandbox
            file_path = os.path.join(self.workspace_dir, filename)

            # Check if the file exists
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "error": f"File {filename} does not exist",
                    "filename": filename
                }

            # Read the file content
            with open(file_path, "r") as f:
                content = f.read()

            return {
                "status": "success",
                "content": content,
                "file_path": file_path,
                "filename": filename
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "filename": filename
            }

    def list_files(self) -> Dict[str, Any]:
        """
        List all files in the sandbox environment.

        Returns:
            A dictionary containing the list of files
        """
        try:
            # List all files in the sandbox
            files = []
            for root, dirs, filenames in os.walk(self.workspace_dir):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, self.workspace_dir)
                    files.append({
                        "filename": rel_path,
                        "path": file_path,
                        "size": os.path.getsize(file_path),
                        "modified_at": os.path.getmtime(file_path)
                    })

            return {
                "status": "success",
                "files": files
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def delete_file(self, filename: str) -> Dict[str, Any]:
        """
        Delete a file from the sandbox environment.

        Args:
            filename: Name of the file to delete

        Returns:
            A dictionary containing the result
        """
        try:
            # Delete a file from the sandbox
            file_path = os.path.join(self.workspace_dir, filename)

            # Check if the file exists
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "error": f"File {filename} does not exist",
                    "filename": filename
                }

            # Delete the file
            os.remove(file_path)

            # Remove from tracked files
            for file_id, file_info in list(self.files.items()):
                if file_info["path"] == file_path:
                    del self.files[file_id]

            return {
                "status": "success",
                "filename": filename
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "filename": filename
            }

    def clean(self) -> Dict[str, Any]:
        """
        Clean the sandbox environment by removing all files.

        Returns:
            A dictionary containing the result
        """
        try:
            # Remove all files in the sandbox
            for root, dirs, filenames in os.walk(self.workspace_dir):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    os.remove(file_path)

            # Clear tracked files
            self.files = {}

            return {
                "status": "success",
                "message": "Sandbox cleaned successfully"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def list_directory(self, path: str = "") -> Dict[str, Any]:
        """
        List contents of a directory in the sandbox.

        Args:
            path: Relative path within the sandbox

        Returns:
            Dictionary with directory contents
        """
        return self.fs.list_directory(path)

    def create_directory(self, path: str) -> Dict[str, Any]:
        """
        Create a directory in the sandbox.

        Args:
            path: Relative path within the sandbox

        Returns:
            Dictionary with operation result
        """
        return self.fs.create_directory(path)

    def copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """
        Copy a file within the sandbox.

        Args:
            source: Source path relative to sandbox
            destination: Destination path relative to sandbox

        Returns:
            Dictionary with operation result
        """
        return self.fs.copy_file(source, destination)

    def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """
        Move a file within the sandbox.

        Args:
            source: Source path relative to sandbox
            destination: Destination path relative to sandbox

        Returns:
            Dictionary with operation result
        """
        return self.fs.move_file(source, destination)

    def find_files(self, pattern: str) -> Dict[str, Any]:
        """
        Find files matching a pattern in the sandbox.

        Args:
            pattern: Glob pattern to match files

        Returns:
            Dictionary with matching files
        """
        return self.fs.find_files(pattern)

    def get_file_info(self, path: str) -> Dict[str, Any]:
        """
        Get information about a file in the sandbox.

        Args:
            path: Relative path within the sandbox

        Returns:
            Dictionary with file information
        """
        return self.fs.get_file_info(path)

# Create a singleton instance
sandbox = Sandbox()

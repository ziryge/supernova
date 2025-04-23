"""
File operations tools for SuperNova AI.
"""

import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import shutil

from ..config.tools import FILE_CONFIG

class FileOperations:
    """File operations tool for managing files."""

    def __init__(self):
        """Initialize the file operations tool."""
        self.allowed_extensions = set(FILE_CONFIG["allowed_extensions"])
        self.max_file_size = FILE_CONFIG["max_file_size"]
        self.output_dir = FILE_CONFIG["output_dir"]

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def read_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read a file and return its contents.

        Args:
            file_path: Path to the file

        Returns:
            A dictionary containing the file contents and metadata
        """
        try:
            file_path = self._normalize_path(file_path)

            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "error": f"File not found: {file_path}",
                    "content": None,
                }

            # Check file extension
            _, ext = os.path.splitext(file_path)
            if ext not in self.allowed_extensions:
                return {
                    "status": "error",
                    "error": f"File extension not allowed: {ext}. Allowed extensions: {', '.join(self.allowed_extensions)}",
                    "content": None,
                }

            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                return {
                    "status": "error",
                    "error": f"File too large: {file_size} bytes. Maximum allowed: {self.max_file_size} bytes",
                    "content": None,
                }

            # Read file
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            return {
                "status": "success",
                "error": "",
                "content": content,
                "size": file_size,
                "path": file_path,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error reading file: {str(e)}",
                "content": None,
            }

    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file.

        Args:
            file_path: Path to the file
            content: Content to write

        Returns:
            A dictionary containing the result of the operation
        """
        try:
            file_path = self._normalize_path(file_path)

            # Check file extension
            _, ext = os.path.splitext(file_path)
            if ext not in self.allowed_extensions:
                return {
                    "status": "error",
                    "error": f"File extension not allowed: {ext}. Allowed extensions: {', '.join(self.allowed_extensions)}",
                }

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "status": "success",
                "error": "",
                "path": file_path,
                "size": len(content),
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error writing file: {str(e)}",
            }

    def list_files(self, directory: str = ".") -> Dict[str, Any]:
        """
        List files in a directory.

        Args:
            directory: Directory to list files from

        Returns:
            A dictionary containing the list of files
        """
        try:
            directory = self._normalize_path(directory)

            # Check if directory exists
            if not os.path.exists(directory):
                return {
                    "status": "error",
                    "error": f"Directory not found: {directory}",
                    "files": [],
                }

            # List files
            files = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                item_stat = os.stat(item_path)

                files.append({
                    "name": item,
                    "path": item_path,
                    "size": item_stat.st_size,
                    "is_dir": os.path.isdir(item_path),
                    "modified": item_stat.st_mtime,
                })

            return {
                "status": "success",
                "error": "",
                "files": files,
                "directory": directory,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error listing files: {str(e)}",
                "files": [],
            }

    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """
        Delete a file.

        Args:
            file_path: Path to the file

        Returns:
            A dictionary containing the result of the operation
        """
        try:
            file_path = self._normalize_path(file_path)

            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "error": f"File not found: {file_path}",
                }

            # Delete file
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

            return {
                "status": "success",
                "error": "",
                "path": file_path,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error deleting file: {str(e)}",
            }

    def _normalize_path(self, path: str) -> str:
        """
        Normalize a file path.

        Args:
            path: File path to normalize

        Returns:
            Normalized file path
        """
        # Convert to absolute path if not already
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        return path

# Create a singleton instance
file_operations = FileOperations()

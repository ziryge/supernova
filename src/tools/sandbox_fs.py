"""
Enhanced file system operations for the SuperNova AI sandbox.
"""

import os
import shutil
import glob
import time
import uuid
from typing import Dict, Any, List, Optional, Union

class SandboxFileSystem:
    """Enhanced file system operations for the sandbox environment."""
    
    def __init__(self, workspace_dir: str):
        """
        Initialize the sandbox file system.
        
        Args:
            workspace_dir: Path to the sandbox workspace directory
        """
        self.workspace_dir = workspace_dir
        
    def list_directory(self, path: str = "") -> Dict[str, Any]:
        """
        List contents of a directory in the sandbox.
        
        Args:
            path: Relative path within the sandbox
            
        Returns:
            Dictionary with directory contents
        """
        try:
            # Normalize the path
            full_path = os.path.join(self.workspace_dir, path)
            
            # Check if the path exists
            if not os.path.exists(full_path):
                return {
                    "status": "error",
                    "error": f"Path {path} does not exist",
                    "path": path
                }
            
            # Check if it's a directory
            if not os.path.isdir(full_path):
                return {
                    "status": "error",
                    "error": f"Path {path} is not a directory",
                    "path": path
                }
            
            # List the directory contents
            items = []
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                rel_path = os.path.join(path, item) if path else item
                
                items.append({
                    "name": item,
                    "path": rel_path,
                    "full_path": item_path,
                    "is_dir": os.path.isdir(item_path),
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0,
                    "modified": os.path.getmtime(item_path)
                })
            
            return {
                "status": "success",
                "path": path,
                "full_path": full_path,
                "items": items
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "path": path
            }
    
    def create_directory(self, path: str) -> Dict[str, Any]:
        """
        Create a directory in the sandbox.
        
        Args:
            path: Relative path within the sandbox
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Normalize the path
            full_path = os.path.join(self.workspace_dir, path)
            
            # Check if the path already exists
            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    return {
                        "status": "success",
                        "message": f"Directory {path} already exists",
                        "path": path,
                        "full_path": full_path
                    }
                else:
                    return {
                        "status": "error",
                        "error": f"Path {path} exists but is not a directory",
                        "path": path
                    }
            
            # Create the directory
            os.makedirs(full_path, exist_ok=True)
            
            return {
                "status": "success",
                "message": f"Directory {path} created successfully",
                "path": path,
                "full_path": full_path
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "path": path
            }
    
    def copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """
        Copy a file within the sandbox.
        
        Args:
            source: Source path relative to sandbox
            destination: Destination path relative to sandbox
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Normalize the paths
            source_path = os.path.join(self.workspace_dir, source)
            dest_path = os.path.join(self.workspace_dir, destination)
            
            # Check if the source exists
            if not os.path.exists(source_path):
                return {
                    "status": "error",
                    "error": f"Source {source} does not exist",
                    "source": source,
                    "destination": destination
                }
            
            # Check if the source is a file
            if not os.path.isfile(source_path):
                return {
                    "status": "error",
                    "error": f"Source {source} is not a file",
                    "source": source,
                    "destination": destination
                }
            
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Copy the file
            shutil.copy2(source_path, dest_path)
            
            return {
                "status": "success",
                "message": f"File {source} copied to {destination}",
                "source": source,
                "destination": destination,
                "source_path": source_path,
                "dest_path": dest_path
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "source": source,
                "destination": destination
            }
    
    def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """
        Move a file within the sandbox.
        
        Args:
            source: Source path relative to sandbox
            destination: Destination path relative to sandbox
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Normalize the paths
            source_path = os.path.join(self.workspace_dir, source)
            dest_path = os.path.join(self.workspace_dir, destination)
            
            # Check if the source exists
            if not os.path.exists(source_path):
                return {
                    "status": "error",
                    "error": f"Source {source} does not exist",
                    "source": source,
                    "destination": destination
                }
            
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Move the file
            shutil.move(source_path, dest_path)
            
            return {
                "status": "success",
                "message": f"File {source} moved to {destination}",
                "source": source,
                "destination": destination,
                "source_path": source_path,
                "dest_path": dest_path
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "source": source,
                "destination": destination
            }
    
    def find_files(self, pattern: str) -> Dict[str, Any]:
        """
        Find files matching a pattern in the sandbox.
        
        Args:
            pattern: Glob pattern to match files
            
        Returns:
            Dictionary with matching files
        """
        try:
            # Normalize the pattern
            full_pattern = os.path.join(self.workspace_dir, pattern)
            
            # Find matching files
            matches = glob.glob(full_pattern)
            
            # Convert to relative paths
            rel_matches = []
            for match in matches:
                rel_path = os.path.relpath(match, self.workspace_dir)
                rel_matches.append({
                    "path": rel_path,
                    "full_path": match,
                    "is_dir": os.path.isdir(match),
                    "size": os.path.getsize(match) if os.path.isfile(match) else 0,
                    "modified": os.path.getmtime(match)
                })
            
            return {
                "status": "success",
                "pattern": pattern,
                "matches": rel_matches,
                "count": len(rel_matches)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "pattern": pattern
            }
    
    def get_file_info(self, path: str) -> Dict[str, Any]:
        """
        Get information about a file in the sandbox.
        
        Args:
            path: Relative path within the sandbox
            
        Returns:
            Dictionary with file information
        """
        try:
            # Normalize the path
            full_path = os.path.join(self.workspace_dir, path)
            
            # Check if the path exists
            if not os.path.exists(full_path):
                return {
                    "status": "error",
                    "error": f"Path {path} does not exist",
                    "path": path
                }
            
            # Get file information
            is_dir = os.path.isdir(full_path)
            
            info = {
                "status": "success",
                "path": path,
                "full_path": full_path,
                "exists": True,
                "is_dir": is_dir,
                "is_file": os.path.isfile(full_path),
                "size": os.path.getsize(full_path) if not is_dir else 0,
                "created": os.path.getctime(full_path),
                "modified": os.path.getmtime(full_path),
                "accessed": os.path.getatime(full_path)
            }
            
            return info
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "path": path
            }

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

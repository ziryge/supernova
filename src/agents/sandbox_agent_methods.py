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

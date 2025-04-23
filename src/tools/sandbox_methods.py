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

"""
Terminal output capture utility for SuperNova AI.
"""

import sys
import io
from typing import Callable, Any, Optional

class TerminalCapture:
    """Capture terminal output and redirect it to a callback function."""
    
    def __init__(self, callback: Callable[[str], Any]):
        """
        Initialize the terminal capture.
        
        Args:
            callback: Function to call with captured output
        """
        self.callback = callback
        self.stdout_capture = io.StringIO()
        self.stderr_capture = io.StringIO()
        self.original_stdout = None
        self.original_stderr = None
    
    def __enter__(self):
        """Start capturing terminal output."""
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self.CaptureStream(self.stdout_capture, self.original_stdout, self.callback)
        sys.stderr = self.CaptureStream(self.stderr_capture, self.original_stderr, self.callback)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop capturing terminal output."""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
    
    def get_output(self) -> str:
        """Get the captured output."""
        return self.stdout_capture.getvalue() + self.stderr_capture.getvalue()
    
    class CaptureStream:
        """Stream that captures output and passes it to a callback function."""
        
        def __init__(self, capture: io.StringIO, original_stream: Optional[io.TextIOWrapper], callback: Callable[[str], Any]):
            """
            Initialize the capture stream.
            
            Args:
                capture: StringIO object to capture output
                original_stream: Original stream to tee output to
                callback: Function to call with captured output
            """
            self.capture = capture
            self.original_stream = original_stream
            self.callback = callback
        
        def write(self, text: str):
            """
            Write text to the stream.
            
            Args:
                text: Text to write
            """
            self.capture.write(text)
            if self.original_stream:
                self.original_stream.write(text)
            
            # Call the callback with the text
            if text.strip():
                self.callback(text)
        
        def flush(self):
            """Flush the stream."""
            self.capture.flush()
            if self.original_stream:
                self.original_stream.flush()

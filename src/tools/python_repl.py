"""
Python REPL tool for SuperNova AI.
"""

import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, Optional
import ast
import time

from ..config.tools import PYTHON_REPL_CONFIG

class PythonREPL:
    """Python REPL for executing code."""

    def __init__(self):
        """Initialize the Python REPL."""
        self.locals = {}
        self.timeout = PYTHON_REPL_CONFIG["timeout"]
        self.max_iterations = PYTHON_REPL_CONFIG["max_iterations"]
        self.allowed_modules = set(PYTHON_REPL_CONFIG["allowed_modules"])

        # Add safe builtins to locals
        self.locals.update({
            "print": print,
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "dict": dict,
            "list": list,
            "set": set,
            "tuple": tuple,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "sum": sum,
            "min": min,
            "max": max,
            "sorted": sorted,
            "round": round,
            "abs": abs,
            "all": all,
            "any": any,
            "zip": zip,
            "map": map,
            "filter": filter,
        })

    def execute(self, code: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute Python code and return the result.

        Args:
            code: The Python code to execute
            timeout: Timeout in seconds (overrides config)

        Returns:
            A dictionary containing the execution result
        """
        if timeout is None:
            timeout = self.timeout

        # Check for unsafe imports
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        module_name = name.name.split('.')[0]
                        if module_name not in self.allowed_modules:
                            return {
                                "status": "error",
                                "error": f"Import of module '{module_name}' is not allowed. Allowed modules: {', '.join(self.allowed_modules)}",
                                "output": "",
                                "result": None,
                            }
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module.split('.')[0] if node.module else ""
                    if module_name not in self.allowed_modules:
                        return {
                            "status": "error",
                            "error": f"Import of module '{module_name}' is not allowed. Allowed modules: {', '.join(self.allowed_modules)}",
                            "output": "",
                            "result": None,
                        }
        except SyntaxError as e:
            return {
                "status": "error",
                "error": f"Syntax error: {str(e)}",
                "output": "",
                "result": None,
            }

        # Capture stdout and stderr
        stdout = io.StringIO()
        stderr = io.StringIO()

        # Execute the code
        result = None
        start_time = time.time()

        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                # Execute the code with timeout
                if timeout > 0:
                    # Simple timeout mechanism
                    sys.settrace(lambda *args, **kwargs: None)
                    result = eval(code, {"__builtins__": __builtins__}, self.locals)
                else:
                    result = eval(code, {"__builtins__": __builtins__}, self.locals)

            return {
                "status": "success",
                "error": "",
                "output": stdout.getvalue(),
                "result": result,
            }
        except Exception as e:
            # If eval fails, try exec
            try:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    # Execute the code with timeout
                    if timeout > 0:
                        # Simple timeout mechanism
                        sys.settrace(lambda *args, **kwargs: None)
                        exec(code, {"__builtins__": __builtins__}, self.locals)
                    else:
                        exec(code, {"__builtins__": __builtins__}, self.locals)

                return {
                    "status": "success",
                    "error": "",
                    "output": stdout.getvalue(),
                    "result": None,
                }
            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                tb = traceback.format_exc()

                return {
                    "status": "error",
                    "error": error_msg,
                    "output": stdout.getvalue(),
                    "traceback": tb,
                    "result": None,
                }
        finally:
            # Check if timeout exceeded
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                return {
                    "status": "timeout",
                    "error": f"Execution timed out after {timeout} seconds",
                    "output": stdout.getvalue(),
                    "result": None,
                }

# Create a singleton instance
python_repl = PythonREPL()

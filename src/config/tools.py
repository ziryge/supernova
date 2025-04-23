"""
Tool configuration for SuperNova AI.
"""

# Web search configuration
SEARCH_CONFIG = {
    "max_results": 5,  # Maximum number of search results to return
    "search_depth": 2,  # How deep to search (1-3)
    "include_domains": [],  # Domains to include in search results
    "exclude_domains": [],  # Domains to exclude from search results
}

# Browser configuration
BROWSER_CONFIG = {
    "headless": True,  # Run browser in headless mode
    "timeout": 30,  # Timeout in seconds for browser operations
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

# Python REPL configuration
PYTHON_REPL_CONFIG = {
    "timeout": 60,  # Timeout in seconds for code execution
    "max_iterations": 5,  # Maximum number of iterations for code execution
    "allowed_modules": [
        "requests", "bs4", "pandas", "numpy", "matplotlib",
        "datetime", "json", "re", "os", "sys", "math", "random",
        "time", "collections", "itertools", "functools"
    ],
}

# File operations configuration
FILE_CONFIG = {
    "allowed_extensions": [
        # Text and documentation
        ".txt", ".md", ".rst", ".log", ".ini", ".cfg", ".conf",
        # Programming languages
        ".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss", ".less",
        ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".go", ".php", ".rb", ".swift",
        ".sh", ".bash", ".zsh", ".bat", ".ps1",
        # Data formats
        ".json", ".yaml", ".yml", ".xml", ".csv", ".tsv", ".toml",
        # Web
        ".html", ".htm", ".css", ".svg",
        # Configuration
        ".env", ".gitignore", ".dockerignore", ".editorconfig",
    ],
    "max_file_size": 20 * 1024 * 1024,  # 20 MB
    "output_dir": "output",
}

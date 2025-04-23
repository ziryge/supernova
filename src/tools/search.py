"""
Web search tools for SuperNova AI.
"""

from typing import List, Dict, Any, Optional
from ..config.env import DEBUG
from ..config.tools import SEARCH_CONFIG

# Import DuckDuckGo search
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

class WebSearch:
    """Web search tool using available search APIs."""

    def __init__(self):
        """Initialize the web search tool."""
        self.max_results = SEARCH_CONFIG["max_results"]
        self.search_depth = SEARCH_CONFIG["search_depth"]

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search the web for information.

        Args:
            query: The search query
            max_results: Maximum number of results to return (overrides config)

        Returns:
            A list of search results
        """
        if max_results is None:
            max_results = self.max_results

        # Print debug information
        if DEBUG:
            print(f"Searching for: {query}")
            print(f"Max results: {max_results}")
            print(f"DuckDuckGo package available: {DDGS_AVAILABLE}")

        # Always use DuckDuckGo if available
        if DDGS_AVAILABLE:
            # If DuckDuckGo package is available, use DuckDuckGo
            if DEBUG:
                print("Using DuckDuckGo search")
            return self._duckduckgo_search(query, max_results)
        else:
            # Otherwise, use a simulated search
            if DEBUG:
                print("Using simulated search")
            return self._simulated_search(query, max_results)

    def _tavily_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Search using Tavily API (deprecated, always falls back to DuckDuckGo).

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            A list of search results from DuckDuckGo
        """
        print("Tavily search is deprecated. Using DuckDuckGo instead.")
        return self._duckduckgo_search(query, max_results)

    def _duckduckgo_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Search using DuckDuckGo.

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            A list of search results
        """
        if not DDGS_AVAILABLE:
            print("DuckDuckGo Search package not installed. Using simulated search.")
            return self._simulated_search(query, max_results)

        try:
            results = []
            with DDGS() as ddgs:
                ddgs_results = list(ddgs.text(query, max_results=max_results))

                for result in ddgs_results:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "content": result.get("body", ""),
                        "score": 0.9,  # DuckDuckGo doesn't provide scores
                    })

            if not results:
                print("No results from DuckDuckGo. Using simulated search.")
                return self._simulated_search(query, max_results)

            return results

        except Exception as e:
            print(f"Error using DuckDuckGo Search: {e}")
            return self._simulated_search(query, max_results)

    def _simulated_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Simulate web search when API is not available.

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            A list of simulated search results
        """
        # Limit the number of results
        num_results = min(max_results, 3)

        results = []
        for i in range(num_results):
            results.append({
                "title": f"Simulated result {i+1} for '{query}'",
                "url": f"https://example.com/simulated-result-{i+1}",
                "content": (
                    f"This is a simulated search result for '{query}'. "
                    "No actual web search was performed because no search API is available. "
                    "Please install the required packages or set the TAVILY_API_KEY environment variable to enable real web search."
                ),
                "score": 0.9 - (i * 0.1),
            })

        return results

# Create a singleton instance
web_search = WebSearch()

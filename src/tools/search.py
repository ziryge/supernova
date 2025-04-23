"""
Web search tools for SuperNova AI.
"""

from typing import List, Dict, Any, Optional
from ..config.env import ToolConfig, DEBUG
from ..config.tools import SEARCH_CONFIG

# Try to import optional dependencies
try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

class WebSearch:
    """Web search tool using available search APIs."""

    def __init__(self):
        """Initialize the web search tool."""
        self.tavily_api_key = ToolConfig.TAVILY_API_KEY
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
            print(f"Tavily API key available: {bool(self.tavily_api_key)}")
            print(f"Tavily package available: {TAVILY_AVAILABLE}")
            print(f"DuckDuckGo package available: {DDGS_AVAILABLE}")

        # Try different search methods in order of preference
        if DDGS_AVAILABLE:
            # If DuckDuckGo package is available, use DuckDuckGo
            if DEBUG:
                print("Using DuckDuckGo search")
            return self._duckduckgo_search(query, max_results)
        elif self.tavily_api_key and TAVILY_AVAILABLE:
            # If Tavily API key is available and package is installed, use Tavily
            if DEBUG:
                print("Using Tavily search")
            return self._tavily_search(query, max_results)
        else:
            # Otherwise, use a simulated search
            if DEBUG:
                print("Using simulated search")
            return self._simulated_search(query, max_results)

    def _tavily_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Search using Tavily API.

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            A list of search results
        """
        if not TAVILY_AVAILABLE:
            print("Tavily package not installed. Using alternative search method.")
            return self._duckduckgo_search(query, max_results)

        try:
            # Use the Tavily client library
            client = TavilyClient(api_key=self.tavily_api_key)

            search_params = {
                "query": query,
                "max_results": max_results,
                "search_depth": self.search_depth,
                "include_domains": SEARCH_CONFIG["include_domains"] or None,
                "exclude_domains": SEARCH_CONFIG["exclude_domains"] or None,
            }

            # Remove None values
            search_params = {k: v for k, v in search_params.items() if v is not None}

            # Execute the search
            response = client.search(**search_params)

            if "results" in response:
                results = response["results"]
                return [
                    {
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", ""),
                        "score": result.get("score", 0),
                    }
                    for result in results
                ]
            else:
                print(f"Tavily API error: {response}")
                return self._duckduckgo_search(query, max_results)

        except Exception as e:
            print(f"Error using Tavily API: {e}")
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

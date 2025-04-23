"""
Streamlit-compatible browser agent for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAgent
from ..tools.streamlit_browser import streamlit_browser

class StreamlitBrowserAgent(BaseAgent):
    """Streamlit-compatible browser agent that navigates websites and extracts information."""

    def __init__(self):
        """Initialize the Streamlit-compatible browser agent."""
        super().__init__("browser", use_reasoning_llm=True)

    def browse(self, url: str) -> Dict[str, Any]:
        """
        Browse a website and extract information.

        Args:
            url: URL to browse

        Returns:
            A dictionary containing the browsing result
        """
        # Navigate to the URL
        result = streamlit_browser.browse(url)

        if result["status"] == "error":
            return {
                "status": "error",
                "error": result["error"],
                "url": url,
                "analysis": f"Failed to navigate to {url}: {result['error']}",
            }

        # Extract the content
        content = result.get("content", "")

        # Ask the LLM to analyze the page
        prompt = f"I need to analyze the content of the webpage at {url}.\n\nHere is the content of the page:\n\n{content[:8000]}...\n\nPlease provide a comprehensive summary of the webpage, including:\n1. The main topic or purpose of the page\n2. Key information presented\n3. Any important details, facts, or figures\n4. The overall structure and organization of the content"

        analysis = self.get_response(prompt)

        return {
            "status": "success",
            "error": "",
            "url": result["url"],
            "title": result["title"],
            "content": content,
            "links": result.get("links", []),
            "analysis": analysis,
            "screenshot": result.get("screenshot"),
        }

    def extract_information(self, url: str, information_request: str) -> Dict[str, Any]:
        """
        Extract specific information from a website.

        Args:
            url: URL to browse
            information_request: Description of the information to extract

        Returns:
            A dictionary containing the extracted information
        """
        # Extract information from the URL
        result = streamlit_browser.extract_information(url, information_request)

        if result["status"] == "error":
            return {
                "status": "error",
                "error": result["error"],
                "url": url,
                "extraction": f"Failed to extract information from {url}: {result['error']}",
            }

        # Extract the content and extracted information
        content = result.get("content", "")
        extracted_info = result.get("extracted_information", "")

        # Ask the LLM to analyze and refine the extracted information
        prompt = f"I need to extract specific information from the webpage at {url}.\n\nInformation requested: {information_request}\n\nHere is the relevant content I found:\n\n{extracted_info}\n\nPlease analyze this information and provide a clear, concise answer to the information request. If the information is not available or incomplete, please indicate that."

        refined_extraction = self.get_response(prompt)

        return {
            "status": "success",
            "error": "",
            "url": result["url"],
            "title": result["title"],
            "information_request": information_request,
            "extraction": refined_extraction,
            "content": content,
            "links": result.get("links", []),
        }

    def search_and_browse(self, query: str) -> Dict[str, Any]:
        """
        Search for information and browse relevant websites.

        Args:
            query: Search query

        Returns:
            A dictionary containing the search and browsing results
        """
        # Search and browse
        result = streamlit_browser.search_and_browse(query)

        if result["status"] == "error":
            return {
                "status": "error",
                "error": result["error"],
                "query": query,
                "analysis": f"Failed to search for {query}: {result['error']}",
            }

        # Extract the content
        content = result.get("content", "")
        search_results = result.get("search_results", [])

        # Format search results for the prompt
        search_results_text = "\n\n".join([
            f"Result {i+1}:\nTitle: {r.get('title', '')}\nURL: {r.get('url', '')}\nSnippet: {r.get('snippet', '')}"
            for i, r in enumerate(search_results[:5])
        ])

        # Ask the LLM to analyze the search results and page content
        prompt = f"I searched for '{query}' and browsed the top result.\n\nSearch Results:\n{search_results_text}\n\nI visited the top result: {result.get('title', '')} ({result.get('url', '')})\n\nHere is the content of the page:\n\n{content[:8000]}...\n\nPlease provide a comprehensive analysis that:\n1. Summarizes the search results\n2. Analyzes the content of the top result\n3. Extracts the most relevant information related to the query\n4. Provides a complete answer to the original query"

        analysis = self.get_response(prompt)

        return {
            "status": "success",
            "error": "",
            "query": query,
            "search_results": search_results,
            "browsed_url": result["url"],
            "title": result["title"],
            "content": content,
            "links": result.get("links", []),
            "analysis": analysis,
            "screenshot": result.get("screenshot"),
        }

    def research_topic(self, topic: str, depth: int = 2) -> Dict[str, Any]:
        """
        Perform in-depth research on a topic by searching and browsing multiple pages.

        Args:
            topic: Topic to research
            depth: Number of pages to browse (default: 2)

        Returns:
            A dictionary containing the research results
        """
        # Search for the topic
        search_result = streamlit_browser.search(topic)

        if search_result["status"] != "success" or not search_result["results"]:
            return {
                "status": "error",
                "error": "No search results found",
                "topic": topic,
                "analysis": f"Failed to find search results for {topic}",
            }

        # Browse the top results
        browsed_pages = []
        for i, result in enumerate(search_result["results"][:depth]):
            if i >= depth:
                break

            url = result["url"]
            browse_result = streamlit_browser.browse(url)

            if browse_result["status"] == "success":
                browsed_pages.append({
                    "url": browse_result["url"],
                    "title": browse_result["title"],
                    "content": browse_result.get("content", ""),
                    "links": browse_result.get("links", []),
                })

        if not browsed_pages:
            return {
                "status": "error",
                "error": "Failed to browse any pages",
                "topic": topic,
                "analysis": f"Failed to browse any pages for {topic}",
            }

        # Format browsed pages for the prompt
        pages_text = "\n\n".join([
            f"Page {i+1}:\nTitle: {p.get('title', '')}\nURL: {p.get('url', '')}\nContent: {p.get('content', '')[:2000]}..."
            for i, p in enumerate(browsed_pages)
        ])

        # Ask the LLM to analyze the research
        prompt = f"I researched the topic '{topic}' by browsing {len(browsed_pages)} web pages.\n\nHere is the content of the pages I visited:\n\n{pages_text}\n\nPlease provide a comprehensive research report that:\n1. Synthesizes information from all sources\n2. Identifies key facts, concepts, and details about the topic\n3. Notes any contradictions or differences between sources\n4. Provides a complete overview of the topic based on all the information gathered"

        analysis = self.get_response(prompt)

        return {
            "status": "success",
            "error": "",
            "topic": topic,
            "search_results": search_result["results"],
            "browsed_pages": browsed_pages,
            "analysis": analysis,
        }

"""
Browser agent for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAgent
from ..tools.browser import web_browser

class BrowserAgent(BaseAgent):
    """Browser agent that navigates websites and extracts information."""

    def __init__(self):
        """Initialize the browser agent."""
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
        result = web_browser.navigate(url)

        if result["status"] == "error":
            return {
                "status": "error",
                "error": result["error"],
                "url": url,
                "analysis": f"Failed to navigate to {url}: {result['error']}",
            }

        # Extract the text content
        text_content = result.get("text_content", "")

        # Ask the LLM to analyze the page
        prompt = f"I need to analyze the content of the webpage at {url}.\n\nHere is the text content of the page:\n\n{text_content[:8000]}...\n\nPlease provide a comprehensive summary of the webpage, including:\n1. The main topic or purpose of the page\n2. Key information presented\n3. Any important details, facts, or figures\n4. The overall structure and organization of the content"

        analysis = self.get_response(prompt)

        return {
            "status": "success",
            "error": "",
            "url": result["url"],
            "title": result["title"],
            "text_content": text_content,
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
        # Navigate to the URL
        result = web_browser.navigate(url)

        if result["status"] == "error":
            return {
                "status": "error",
                "error": result["error"],
                "url": url,
                "extraction": f"Failed to navigate to {url}: {result['error']}",
            }

        # Extract the text content
        text_content = result.get("text_content", "")

        # Ask the LLM to extract the requested information
        prompt = f"I need to extract specific information from the webpage at {url}.\n\nHere is the text content of the page:\n\n{text_content[:8000]}...\n\nI need to extract the following information:\n{information_request}\n\nPlease provide the requested information in a clear and structured format. If the information is not available on the page, please indicate that."

        extraction = self.get_response(prompt)

        return {
            "status": "success",
            "error": "",
            "url": result["url"],
            "title": result["title"],
            "extraction": extraction,
        }

    def interact(self, url: str, interaction_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Interact with a website by performing a series of actions.

        Args:
            url: URL to browse
            interaction_steps: List of interaction steps to perform

        Returns:
            A dictionary containing the interaction result
        """
        # Navigate to the URL
        result = web_browser.navigate(url)

        if result["status"] == "error":
            return {
                "status": "error",
                "error": result["error"],
                "url": url,
                "interaction_results": [],
                "final_state": f"Failed to navigate to {url}: {result['error']}",
            }

        # Perform each interaction step
        interaction_results = []
        current_url = result["url"]
        current_title = result["title"]

        for step in interaction_steps:
            step_type = step.get("type", "")

            if step_type == "click":
                # Click an element
                selector = step.get("selector", "")
                click_result = web_browser.click(selector)

                interaction_results.append({
                    "step": step,
                    "result": click_result,
                })

                if click_result["status"] == "success":
                    current_url = click_result["url"]
                    current_title = click_result["title"]

            elif step_type == "fill":
                # Fill a form field
                form_data = {step.get("selector", ""): step.get("value", "")}
                fill_result = web_browser.fill_form(form_data)

                interaction_results.append({
                    "step": step,
                    "result": fill_result,
                })

            elif step_type == "submit":
                # Submit a form
                selector = step.get("selector", "")
                submit_result = web_browser.submit_form(selector)

                interaction_results.append({
                    "step": step,
                    "result": submit_result,
                })

                if submit_result["status"] == "success":
                    current_url = submit_result["url"]
                    current_title = submit_result["title"]

            elif step_type == "extract":
                # Extract content
                selector = step.get("selector", "")
                extract_result = web_browser.extract_content(selector)

                interaction_results.append({
                    "step": step,
                    "result": extract_result,
                })

        # Take a screenshot of the final state
        screenshot_result = web_browser.take_screenshot()

        # Get the final page content
        final_result = web_browser.navigate(current_url)
        final_text_content = final_result.get("text_content", "") if final_result["status"] == "success" else ""

        # Ask the LLM to analyze the final state
        prompt = f"I performed a series of interactions on the webpage at {url}, and now I'm at {current_url} with title '{current_title}'.\n\nHere is the text content of the final page:\n\n{final_text_content[:8000]}...\n\nPlease provide a summary of the current state of the page and the result of the interactions."

        final_analysis = self.get_response(prompt)

        return {
            "status": "success",
            "error": "",
            "url": url,
            "final_url": current_url,
            "final_title": current_title,
            "interaction_results": interaction_results,
            "final_state": final_analysis,
            "screenshot": screenshot_result.get("screenshot") if screenshot_result["status"] == "success" else None,
        }

    def search_and_browse(self, query: str) -> Dict[str, Any]:
        """
        Search for information and browse relevant websites.

        Args:
            query: Search query

        Returns:
            A dictionary containing the search and browsing results
        """
        from ..tools.search import web_search

        # Perform a web search
        search_results = web_search.search(query)

        if not search_results:
            return {
                "status": "error",
                "error": "No search results found",
                "query": query,
                "analysis": f"No search results found for query: {query}",
            }

        # Browse the top result
        top_result = search_results[0]
        url = top_result["url"]

        browse_result = self.browse(url)

        # Combine the search and browsing results
        combined_analysis = f"Search query: {query}\n\nTop result: {top_result['title']} ({url})\n\n{browse_result['analysis']}"

        return {
            "status": "success",
            "error": "",
            "query": query,
            "search_results": search_results,
            "browsed_url": url,
            "browse_result": browse_result,
            "analysis": combined_analysis,
        }

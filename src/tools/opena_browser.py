"""
Enhanced browser tools for SuperNova AI.
"""

import os
import time
import tempfile
import json
import re
import base64
from typing import Dict, Any, List, Optional, Union
from urllib.parse import urlparse, urljoin, quote_plus
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import html2text

from ..config.env import ToolConfig, DEBUG
from ..config.tools import BROWSER_CONFIG
from .search import web_search

# Try to import optional dependencies
try:
    from playwright.sync_api import sync_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class OpenaBrowser:
    """Enhanced browser tool for SuperNova AI."""

    def __init__(self):
        """Initialize the SuperNova browser tool."""
        # Always set headless to False to make the browser visible
        self.headless = False
        self.timeout = BROWSER_CONFIG.get("timeout", 30)
        self.user_agent = BROWSER_CONFIG.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        # Initialize browser instance variables
        self.browser = None
        self.page = None
        self.playwright = None

        # Initialize HTML to text converter
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.ignore_tables = False
        self.html_converter.body_width = 0  # No wrapping

        # Initialize session history
        self.session_history = []
        self.current_page_info = None

        if DEBUG:
            print(f"SuperNova browser tool initialized")

    def _initialize_browser(self):
        """Initialize the browser if not already initialized."""
        if not PLAYWRIGHT_AVAILABLE:
            print("Playwright is not available. Please install it with 'pip install playwright' and 'playwright install'.")
            return False

        if not self.browser:
            try:
                print("Launching Chromium browser with Playwright...")
                self.playwright = sync_playwright().start()

                # Launch Chromium with visible browser window
                self.browser = self.playwright.chromium.launch(
                    headless=self.headless,  # This should be False from our init
                    args=['--start-maximized']  # Start with maximized window
                )

                print(f"Browser launched successfully. Headless mode: {self.headless}")

                # Create a new page with custom viewport and user agent
                self.page = self.browser.new_page(
                    user_agent=self.user_agent,
                    viewport={"width": 1280, "height": 800}  # Set a reasonable viewport size
                )

                self.page.set_default_timeout(self.timeout * 1000)  # Convert to milliseconds

                # Set up event listeners
                self.page.on("response", self._handle_response)

                print("Browser initialization complete. Ready for browsing.")
                return True
            except Exception as e:
                print(f"Error initializing Playwright browser: {e}")
                return False

        return True

    def _handle_response(self, response):
        """Handle response events from the browser."""
        if response.status >= 400:
            if DEBUG:
                print(f"Error response: {response.status} {response.url}")

    def _close_browser(self):
        """Close the browser."""
        if self.browser:
            try:
                self.browser.close()
                self.playwright.stop()
                self.browser = None
                self.page = None
                self.playwright = None
            except Exception as e:
                print(f"Error closing browser: {e}")

    def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            A dictionary containing the search results
        """
        # Use the web_search tool to perform the search
        search_results = web_search.search(query, num_results)

        # Process the search results
        processed_results = []
        for result in search_results:
            processed_results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("content", "")[:300] + "..." if len(result.get("content", "")) > 300 else result.get("content", ""),
                "source": "search",
            })

        return {
            "status": "success",
            "query": query,
            "results": processed_results,
        }

    def browse(self, url: str) -> Dict[str, Any]:
        """
        Browse a webpage and extract its content.

        Args:
            url: URL to browse

        Returns:
            A dictionary containing the page content and metadata
        """
        # Validate URL
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        print(f"Browsing URL: {url}")

        # Always use the browser for a visible browsing experience
        return self._browse_with_browser(url)

    def _browse_with_browser(self, url: str) -> Dict[str, Any]:
        """
        Browse a webpage using the browser.

        Args:
            url: URL to browse

        Returns:
            A dictionary containing the page content and metadata
        """
        # Initialize browser if needed
        if not self._initialize_browser():
            print("Failed to initialize browser. Please check Playwright installation.")
            return {
                "status": "error",
                "error": "Failed to initialize browser",
                "url": url,
            }

        try:
            print(f"Navigating to {url} with Chromium browser...")
            # Navigate to the URL
            self.page.goto(url)

            print("Waiting for page to load completely...")
            # Wait for page to load
            self.page.wait_for_load_state("networkidle")

            # Get page info
            title = self.page.title()
            current_url = self.page.url
            print(f"Page loaded: {title} ({current_url})")

            # Pause to allow user to see the page (3 seconds)
            print("Pausing for 3 seconds to allow viewing the page...")
            time.sleep(3)

            # Extract HTML content
            print("Extracting page content...")
            html_content = self.page.content()

            # Parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract main content
            main_content = self._extract_main_content(soup)

            # Convert HTML to markdown
            markdown_content = self.html_converter.handle(main_content)

            # Extract links
            links = self._extract_links(soup, current_url)
            print(f"Extracted {len(links)} links from the page")

            # Take screenshot
            print("Taking screenshot...")
            screenshot = self._take_screenshot()

            # Add to session history
            page_info = {
                "url": current_url,
                "title": title,
                "timestamp": time.time(),
            }
            self.session_history.append(page_info)
            self.current_page_info = page_info

            print("Browsing complete. Returning page content.")
            return {
                "status": "success",
                "url": current_url,
                "title": title,
                "content": markdown_content,
                "html": main_content,
                "links": links,
                "screenshot": screenshot,
                "method": "browser",
            }

        except Exception as e:
            error_msg = f"Error browsing {url}: {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
                "url": url,
            }

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract the main content from a webpage.

        Args:
            soup: BeautifulSoup object

        Returns:
            HTML string of the main content
        """
        # Try to find the main content
        main_tags = [
            soup.find("main"),
            soup.find(id="main"),
            soup.find(id="content"),
            soup.find(id="main-content"),
            soup.find(class_="main"),
            soup.find(class_="content"),
            soup.find(class_="main-content"),
            soup.find("article"),
        ]

        # Use the first valid main tag found
        for tag in main_tags:
            if tag:
                return str(tag)

        # If no main content found, use the body
        body = soup.find("body")
        if body:
            # Remove script and style tags
            for script in body(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            return str(body)

        # If no body found, use the whole HTML
        return str(soup)

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """
        Extract links from a webpage.

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links

        Returns:
            List of dictionaries containing link information
        """
        links = []

        # Find all links
        for a in soup.find_all("a", href=True):
            href = a["href"]

            # Skip empty links, javascript links, and anchors
            if not href or href.startswith(("javascript:", "#", "mailto:", "tel:")):
                continue

            # Resolve relative URLs
            if not href.startswith(("http://", "https://")):
                href = urljoin(base_url, href)

            # Extract text
            text = a.get_text().strip()
            if not text:
                text = href

            links.append({
                "url": href,
                "text": text,
            })

        return links

    def click(self, link_text: str) -> Dict[str, Any]:
        """
        Click a link on the current page.

        Args:
            link_text: Text of the link to click

        Returns:
            A dictionary containing the result of the operation
        """
        # Check if browser is initialized
        if not self.browser or not self.page:
            return {
                "status": "error",
                "error": "Browser not initialized",
            }

        try:
            # Try to find the link by text
            link = self.page.get_by_text(link_text, exact=False)

            # Click the link
            link.click()

            # Wait for navigation to complete
            self.page.wait_for_load_state("networkidle")

            # Get page info
            title = self.page.title()
            current_url = self.page.url

            # Extract HTML content
            html_content = self.page.content()

            # Parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract main content
            main_content = self._extract_main_content(soup)

            # Convert HTML to markdown
            markdown_content = self.html_converter.handle(main_content)

            # Extract links
            links = self._extract_links(soup, current_url)

            # Take screenshot
            screenshot = self._take_screenshot()

            # Add to session history
            page_info = {
                "url": current_url,
                "title": title,
                "timestamp": time.time(),
            }
            self.session_history.append(page_info)
            self.current_page_info = page_info

            return {
                "status": "success",
                "url": current_url,
                "title": title,
                "content": markdown_content,
                "html": main_content,
                "links": links,
                "screenshot": screenshot,
            }

        except Exception as e:
            error_msg = f"Error clicking link '{link_text}': {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
            }

    def back(self) -> Dict[str, Any]:
        """
        Go back to the previous page.

        Returns:
            A dictionary containing the result of the operation
        """
        # Check if browser is initialized
        if not self.browser or not self.page:
            return {
                "status": "error",
                "error": "Browser not initialized",
            }

        try:
            # Go back
            self.page.go_back()

            # Wait for navigation to complete
            self.page.wait_for_load_state("networkidle")

            # Get page info
            title = self.page.title()
            current_url = self.page.url

            # Extract HTML content
            html_content = self.page.content()

            # Parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract main content
            main_content = self._extract_main_content(soup)

            # Convert HTML to markdown
            markdown_content = self.html_converter.handle(main_content)

            # Extract links
            links = self._extract_links(soup, current_url)

            # Take screenshot
            screenshot = self._take_screenshot()

            # Update current page info
            if len(self.session_history) >= 2:
                self.current_page_info = self.session_history[-2]

            return {
                "status": "success",
                "url": current_url,
                "title": title,
                "content": markdown_content,
                "html": main_content,
                "links": links,
                "screenshot": screenshot,
            }

        except Exception as e:
            error_msg = f"Error going back: {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
            }

    def search_and_browse(self, query: str) -> Dict[str, Any]:
        """
        Search for a query and browse the top result.

        Args:
            query: Search query

        Returns:
            A dictionary containing the search and browse results
        """
        # Search for the query
        search_result = self.search(query)

        if search_result["status"] != "success" or not search_result["results"]:
            return {
                "status": "error",
                "error": "No search results found",
                "query": query,
            }

        # Get the top result
        top_result = search_result["results"][0]
        url = top_result["url"]

        # Browse the top result
        browse_result = self.browse(url)

        return {
            "status": browse_result["status"],
            "query": query,
            "search_results": search_result["results"],
            "top_result": top_result,
            "browse_result": browse_result,
            "url": browse_result.get("url", url),
            "title": browse_result.get("title", top_result["title"]),
            "content": browse_result.get("content", ""),
            "links": browse_result.get("links", []),
            "screenshot": browse_result.get("screenshot", None),
        }

    def extract_information(self, url: str, information_request: str) -> Dict[str, Any]:
        """
        Extract specific information from a webpage.

        Args:
            url: URL to browse
            information_request: Description of the information to extract

        Returns:
            A dictionary containing the extracted information
        """
        # Browse the webpage
        browse_result = self.browse(url)

        if browse_result["status"] != "success":
            return {
                "status": "error",
                "error": browse_result["error"],
                "url": url,
                "information_request": information_request,
            }

        # Extract the requested information using pattern matching
        content = browse_result["content"]

        # Create a summary of the extracted information
        summary = self._extract_information_from_content(content, information_request)

        return {
            "status": "success",
            "url": browse_result["url"],
            "title": browse_result["title"],
            "information_request": information_request,
            "extracted_information": summary,
            "content": content,
            "links": browse_result.get("links", []),
            "screenshot": browse_result.get("screenshot", None),
        }

    def _extract_information_from_content(self, content: str, information_request: str) -> str:
        """
        Extract specific information from content.

        Args:
            content: Content to extract information from
            information_request: Description of the information to extract

        Returns:
            Extracted information as a string
        """
        # This is a placeholder for more sophisticated extraction
        # In a real implementation, this would use NLP or other techniques

        # For now, we'll just return relevant sections of the content
        # based on keyword matching

        # Extract keywords from the information request
        keywords = re.findall(r'\b\w+\b', information_request.lower())
        keywords = [k for k in keywords if len(k) > 3 and k not in ["what", "when", "where", "which", "about", "information"]]

        # Split content into paragraphs
        paragraphs = content.split("\n\n")

        # Score each paragraph based on keyword matches
        scored_paragraphs = []
        for p in paragraphs:
            if len(p.strip()) < 10:  # Skip very short paragraphs
                continue

            score = sum(1 for k in keywords if k in p.lower())
            if score > 0:
                scored_paragraphs.append((score, p))

        # Sort by score (highest first)
        scored_paragraphs.sort(reverse=True)

        # Take the top 5 paragraphs
        top_paragraphs = [p for _, p in scored_paragraphs[:5]]

        if not top_paragraphs:
            return "Could not find specific information related to your request."

        # Join the paragraphs
        return "\n\n".join(top_paragraphs)

    def _take_screenshot(self) -> Optional[str]:
        """
        Take a screenshot of the current page.

        Returns:
            Base64-encoded screenshot or None if failed
        """
        if not self.browser or not self.page:
            return None

        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name

            # Take screenshot
            self.page.screenshot(path=tmp_path)

            # Read the file and convert to base64
            with open(tmp_path, "rb") as f:
                screenshot_data = f.read()

            # Remove the temporary file
            os.unlink(tmp_path)

            # Convert to base64
            return base64.b64encode(screenshot_data).decode("utf-8")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None

    def close(self):
        """Close the browser."""
        self._close_browser()

# Create a singleton instance
opena_browser = OpenaBrowser()

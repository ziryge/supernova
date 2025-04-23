"""
Streamlit-compatible browser tools for SuperNova AI.
This version is designed to work in Streamlit Cloud environments.
"""

import os
import time
import json
import re
from typing import Dict, Any, List, Optional, Union
from urllib.parse import urlparse, urljoin, quote_plus
import requests
from bs4 import BeautifulSoup
import html2text

from ..config.env import ToolConfig, DEBUG
from ..config.tools import BROWSER_CONFIG
from .search import web_search

class StreamlitBrowser:
    """Streamlit-compatible browser tool for SuperNova AI."""

    def __init__(self):
        """Initialize the Streamlit-compatible browser tool."""
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
            print(f"SuperNova Streamlit browser tool initialized")

    def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            A dictionary containing the search results
        """
        try:
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
        except Exception as e:
            error_msg = f"Error searching for '{query}': {str(e)}"
            print(error_msg)
            return {
                "status": "error",
                "error": error_msg,
                "query": query,
                "results": [],
            }

    def browse(self, url: str) -> Dict[str, Any]:
        """
        Browse a webpage and extract its content using requests.

        Args:
            url: URL to browse

        Returns:
            A dictionary containing the page content and metadata
        """
        # Validate URL
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        print(f"Browsing URL: {url}")

        try:
            # Set up headers
            headers = {
                "User-Agent": BROWSER_CONFIG.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }

            # Make the request
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses

            # Get the final URL (after redirects)
            final_url = response.url

            # Parse the HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Get the title
            title = soup.title.string if soup.title else url

            # Extract main content
            main_content = self._extract_main_content(soup)

            # Convert HTML to markdown
            markdown_content = self.html_converter.handle(main_content)

            # Extract links
            links = self._extract_links(soup, final_url)
            print(f"Extracted {len(links)} links from the page")

            # Add to session history
            page_info = {
                "url": final_url,
                "title": title,
                "timestamp": time.time(),
            }
            self.session_history.append(page_info)
            self.current_page_info = page_info

            print("Browsing complete. Returning page content.")
            return {
                "status": "success",
                "url": final_url,
                "title": title,
                "content": markdown_content,
                "html": main_content,
                "links": links,
                "screenshot": None,  # No screenshot in this version
                "method": "requests",
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
            "screenshot": None,  # No screenshot in this version
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
            "screenshot": None,  # No screenshot in this version
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

# Create a singleton instance
streamlit_browser = StreamlitBrowser()

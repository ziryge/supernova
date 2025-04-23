"""
Browser tools for SuperNova AI.
"""

import os
import time
import tempfile
from typing import Dict, Any, List, Optional, Union
from urllib.parse import urlparse
import base64
from pathlib import Path
import json

from ..config.env import ToolConfig, DEBUG
from ..config.tools import BROWSER_CONFIG

# Try to import optional dependencies
try:
    from playwright.sync_api import sync_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class WebBrowser:
    """Web browser tool for browsing websites."""

    def __init__(self):
        """Initialize the web browser tool."""
        self.browser_type = "playwright" if PLAYWRIGHT_AVAILABLE else "selenium" if SELENIUM_AVAILABLE else None
        self.headless = BROWSER_CONFIG.get("headless", True)
        self.timeout = BROWSER_CONFIG.get("timeout", 30)
        self.user_agent = BROWSER_CONFIG.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        # Initialize browser instance variables
        self.browser = None
        self.page = None
        self.driver = None

        if DEBUG:
            print(f"Browser tool initialized with {self.browser_type}")

    def _initialize_browser(self):
        """Initialize the browser if not already initialized."""
        if self.browser_type == "playwright" and not self.browser:
            try:
                self.playwright = sync_playwright().start()
                self.browser = self.playwright.chromium.launch(headless=self.headless)
                self.page = self.browser.new_page(user_agent=self.user_agent)
                self.page.set_default_timeout(self.timeout * 1000)  # Convert to milliseconds
                return True
            except Exception as e:
                print(f"Error initializing Playwright browser: {e}")
                self.browser_type = "selenium" if SELENIUM_AVAILABLE else None
                return self._initialize_browser()

        elif self.browser_type == "selenium" and not self.driver:
            try:
                options = Options()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument(f"user-agent={self.user_agent}")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")

                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                self.driver.set_page_load_timeout(self.timeout)
                return True
            except Exception as e:
                print(f"Error initializing Selenium browser: {e}")
                self.browser_type = None
                return False

        elif not self.browser_type:
            print("No browser implementation available. Please install playwright or selenium.")
            return False

        return True

    def _close_browser(self):
        """Close the browser."""
        if self.browser_type == "playwright" and self.browser:
            try:
                self.browser.close()
                self.playwright.stop()
                self.browser = None
                self.page = None
                self.playwright = None
            except Exception as e:
                print(f"Error closing Playwright browser: {e}")

        elif self.browser_type == "selenium" and self.driver:
            try:
                self.driver.quit()
                self.driver = None
            except Exception as e:
                print(f"Error closing Selenium browser: {e}")

    def navigate(self, url: str) -> Dict[str, Any]:
        """
        Navigate to a URL.

        Args:
            url: URL to navigate to

        Returns:
            A dictionary containing the page content and metadata
        """
        # Validate URL
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        # Initialize browser if needed
        if not self._initialize_browser():
            return {
                "status": "error",
                "error": "Failed to initialize browser",
                "content": "",
                "title": "",
                "url": url,
            }

        try:
            if self.browser_type == "playwright":
                self.page.goto(url)

                # Wait for page to load
                self.page.wait_for_load_state("networkidle")

                # Get page content
                content = self.page.content()
                title = self.page.title()
                current_url = self.page.url

                # Extract text content
                text_content = self.page.evaluate("() => document.body.innerText")

                # Take screenshot
                screenshot = self._take_screenshot_playwright()

                return {
                    "status": "success",
                    "error": "",
                    "content": content,
                    "text_content": text_content,
                    "title": title,
                    "url": current_url,
                    "screenshot": screenshot,
                }

            elif self.browser_type == "selenium":
                self.driver.get(url)

                # Wait for page to load
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Get page content
                content = self.driver.page_source
                title = self.driver.title
                current_url = self.driver.current_url

                # Extract text content
                text_content = self.driver.find_element(By.TAG_NAME, "body").text

                # Take screenshot
                screenshot = self._take_screenshot_selenium()

                return {
                    "status": "success",
                    "error": "",
                    "content": content,
                    "text_content": text_content,
                    "title": title,
                    "url": current_url,
                    "screenshot": screenshot,
                }

            else:
                return {
                    "status": "error",
                    "error": "No browser implementation available",
                    "content": "",
                    "title": "",
                    "url": url,
                }

        except Exception as e:
            error_msg = f"Error navigating to {url}: {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
                "content": "",
                "title": "",
                "url": url,
            }

    def extract_content(self, selector: str) -> Dict[str, Any]:
        """
        Extract content from the current page using a CSS selector.

        Args:
            selector: CSS selector to extract content from

        Returns:
            A dictionary containing the extracted content
        """
        if not self._is_browser_active():
            return {
                "status": "error",
                "error": "Browser not initialized or no page loaded",
                "content": "",
            }

        try:
            if self.browser_type == "playwright":
                # Check if selector exists
                element_count = self.page.evaluate(f"document.querySelectorAll('{selector}').length")

                if element_count == 0:
                    return {
                        "status": "error",
                        "error": f"Selector '{selector}' not found on page",
                        "content": "",
                    }

                # Extract content
                content = self.page.evaluate(f"""() => {{
                    const elements = document.querySelectorAll('{selector}');
                    return Array.from(elements).map(el => el.outerHTML);
                }}""")

                # Extract text content
                text_content = self.page.evaluate(f"""() => {{
                    const elements = document.querySelectorAll('{selector}');
                    return Array.from(elements).map(el => el.innerText);
                }}""")

                return {
                    "status": "success",
                    "error": "",
                    "content": content,
                    "text_content": text_content,
                    "count": element_count,
                }

            elif self.browser_type == "selenium":
                # Find elements
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

                if not elements:
                    return {
                        "status": "error",
                        "error": f"Selector '{selector}' not found on page",
                        "content": "",
                    }

                # Extract content
                content = [element.get_attribute("outerHTML") for element in elements]

                # Extract text content
                text_content = [element.text for element in elements]

                return {
                    "status": "success",
                    "error": "",
                    "content": content,
                    "text_content": text_content,
                    "count": len(elements),
                }

            else:
                return {
                    "status": "error",
                    "error": "No browser implementation available",
                    "content": "",
                }

        except Exception as e:
            error_msg = f"Error extracting content with selector '{selector}': {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
                "content": "",
            }

    def click(self, selector: str) -> Dict[str, Any]:
        """
        Click an element on the current page.

        Args:
            selector: CSS selector of the element to click

        Returns:
            A dictionary containing the result of the operation
        """
        if not self._is_browser_active():
            return {
                "status": "error",
                "error": "Browser not initialized or no page loaded",
            }

        try:
            if self.browser_type == "playwright":
                # Check if selector exists
                element_count = self.page.evaluate(f"document.querySelectorAll('{selector}').length")

                if element_count == 0:
                    return {
                        "status": "error",
                        "error": f"Selector '{selector}' not found on page",
                    }

                # Click the element
                self.page.click(selector)

                # Wait for navigation to complete
                self.page.wait_for_load_state("networkidle")

                return {
                    "status": "success",
                    "error": "",
                    "title": self.page.title(),
                    "url": self.page.url,
                }

            elif self.browser_type == "selenium":
                # Find element
                try:
                    element = WebDriverWait(self.driver, self.timeout).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                except Exception:
                    return {
                        "status": "error",
                        "error": f"Selector '{selector}' not found or not clickable",
                    }

                # Click the element
                element.click()

                # Wait for page to load
                time.sleep(2)  # Simple wait for any potential navigation

                return {
                    "status": "success",
                    "error": "",
                    "title": self.driver.title,
                    "url": self.driver.current_url,
                }

            else:
                return {
                    "status": "error",
                    "error": "No browser implementation available",
                }

        except Exception as e:
            error_msg = f"Error clicking element with selector '{selector}': {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
            }

    def fill_form(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Fill a form on the current page.

        Args:
            form_data: Dictionary mapping selectors to values

        Returns:
            A dictionary containing the result of the operation
        """
        if not self._is_browser_active():
            return {
                "status": "error",
                "error": "Browser not initialized or no page loaded",
            }

        try:
            results = {}

            for selector, value in form_data.items():
                if self.browser_type == "playwright":
                    try:
                        # Check if selector exists
                        element_count = self.page.evaluate(f"document.querySelectorAll('{selector}').length")

                        if element_count == 0:
                            results[selector] = {
                                "status": "error",
                                "error": f"Selector '{selector}' not found on page",
                            }
                            continue

                        # Fill the form field
                        self.page.fill(selector, value)

                        results[selector] = {
                            "status": "success",
                            "error": "",
                        }
                    except Exception as e:
                        results[selector] = {
                            "status": "error",
                            "error": str(e),
                        }

                elif self.browser_type == "selenium":
                    try:
                        # Find element
                        element = WebDriverWait(self.driver, self.timeout).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )

                        # Clear existing value
                        element.clear()

                        # Fill the form field
                        element.send_keys(value)

                        results[selector] = {
                            "status": "success",
                            "error": "",
                        }
                    except Exception as e:
                        results[selector] = {
                            "status": "error",
                            "error": str(e),
                        }

            return {
                "status": "success" if all(r["status"] == "success" for r in results.values()) else "partial",
                "error": "",
                "results": results,
            }

        except Exception as e:
            error_msg = f"Error filling form: {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
            }

    def submit_form(self, form_selector: str) -> Dict[str, Any]:
        """
        Submit a form on the current page.

        Args:
            form_selector: CSS selector of the form to submit

        Returns:
            A dictionary containing the result of the operation
        """
        if not self._is_browser_active():
            return {
                "status": "error",
                "error": "Browser not initialized or no page loaded",
            }

        try:
            if self.browser_type == "playwright":
                # Check if selector exists
                element_count = self.page.evaluate(f"document.querySelectorAll('{form_selector}').length")

                if element_count == 0:
                    return {
                        "status": "error",
                        "error": f"Form selector '{form_selector}' not found on page",
                    }

                # Submit the form
                self.page.evaluate(f"document.querySelector('{form_selector}').submit()")

                # Wait for navigation to complete
                self.page.wait_for_load_state("networkidle")

                return {
                    "status": "success",
                    "error": "",
                    "title": self.page.title(),
                    "url": self.page.url,
                }

            elif self.browser_type == "selenium":
                # Find form
                try:
                    form = WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, form_selector))
                    )
                except Exception:
                    return {
                        "status": "error",
                        "error": f"Form selector '{form_selector}' not found",
                    }

                # Submit the form
                form.submit()

                # Wait for page to load
                time.sleep(2)  # Simple wait for any potential navigation

                return {
                    "status": "success",
                    "error": "",
                    "title": self.driver.title,
                    "url": self.driver.current_url,
                }

            else:
                return {
                    "status": "error",
                    "error": "No browser implementation available",
                }

        except Exception as e:
            error_msg = f"Error submitting form with selector '{form_selector}': {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
            }

    def take_screenshot(self) -> Dict[str, Any]:
        """
        Take a screenshot of the current page.

        Returns:
            A dictionary containing the screenshot data
        """
        if not self._is_browser_active():
            return {
                "status": "error",
                "error": "Browser not initialized or no page loaded",
                "screenshot": None,
            }

        try:
            if self.browser_type == "playwright":
                screenshot = self._take_screenshot_playwright()
            elif self.browser_type == "selenium":
                screenshot = self._take_screenshot_selenium()
            else:
                return {
                    "status": "error",
                    "error": "No browser implementation available",
                    "screenshot": None,
                }

            return {
                "status": "success",
                "error": "",
                "screenshot": screenshot,
            }

        except Exception as e:
            error_msg = f"Error taking screenshot: {str(e)}"
            print(error_msg)

            return {
                "status": "error",
                "error": error_msg,
                "screenshot": None,
            }

    def _take_screenshot_playwright(self) -> Optional[str]:
        """Take a screenshot using Playwright and return as base64."""
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
            print(f"Error taking screenshot with Playwright: {e}")
            return None

    def _take_screenshot_selenium(self) -> Optional[str]:
        """Take a screenshot using Selenium and return as base64."""
        try:
            # Take screenshot
            screenshot_data = self.driver.get_screenshot_as_png()

            # Convert to base64
            return base64.b64encode(screenshot_data).decode("utf-8")
        except Exception as e:
            print(f"Error taking screenshot with Selenium: {e}")
            return None

    def _is_browser_active(self) -> bool:
        """Check if the browser is active and a page is loaded."""
        if self.browser_type == "playwright":
            return self.browser is not None and self.page is not None
        elif self.browser_type == "selenium":
            return self.driver is not None
        else:
            return False

    def close(self):
        """Close the browser."""
        self._close_browser()

# Create a singleton instance
web_browser = WebBrowser()

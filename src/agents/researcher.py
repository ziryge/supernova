"""
Researcher agent for SuperNova AI.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAgent
from ..tools.search import web_search

class ResearcherAgent(BaseAgent):
    """Researcher agent that gathers information."""

    def __init__(self):
        """Initialize the researcher agent."""
        super().__init__("researcher", use_reasoning_llm=True)

    def search(self, query: str, max_results: Optional[int] = None) -> Dict[str, Any]:
        """
        Search for information on a topic.

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            A dictionary containing the search results and analysis
        """
        # Perform the search
        search_results = web_search.search(query, max_results)

        # Format the search results for the LLM
        formatted_results = self._format_search_results(search_results)

        # Ask the LLM to analyze the results
        prompt = f"I need to research the following topic:\n\n{query}\n\nHere are the search results:\n\n{formatted_results}\n\nPlease analyze these results and provide a comprehensive summary of the information. Include key facts, different perspectives, and any important details."

        analysis = self.get_response(prompt)

        return {
            "query": query,
            "results": search_results,
            "analysis": analysis,
        }

    def extract_information(self, text: str, questions: List[str]) -> Dict[str, Any]:
        """
        Extract specific information from text.

        Args:
            text: Text to extract information from
            questions: List of questions to answer

        Returns:
            A dictionary containing the extracted information
        """
        # Format the questions
        formatted_questions = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])

        # Ask the LLM to extract the information
        prompt = f"I need to extract specific information from the following text:\n\n{text}\n\nPlease answer these questions based on the text:\n\n{formatted_questions}\n\nProvide direct answers with relevant quotes or evidence from the text."

        extraction = self.get_response(prompt)

        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "questions": questions,
            "extraction": extraction,
        }

    def compare_sources(self, sources: List[Dict[str, Any]], topic: str) -> Dict[str, Any]:
        """
        Compare information from multiple sources.

        Args:
            sources: List of sources to compare
            topic: Topic being researched

        Returns:
            A dictionary containing the comparison
        """
        # Format the sources
        formatted_sources = ""
        for i, source in enumerate(sources, 1):
            formatted_sources += f"Source {i}: {source.get('title', 'Untitled')}\n"
            formatted_sources += f"URL: {source.get('url', 'No URL')}\n"
            formatted_sources += f"Content: {source.get('content', 'No content')[:200]}...\n\n"

        # Ask the LLM to compare the sources
        prompt = f"I need to compare information from multiple sources on the topic of '{topic}':\n\n{formatted_sources}\n\nPlease compare these sources and identify:\n1. Points of agreement\n2. Points of disagreement\n3. Unique information from each source\n4. Overall reliability assessment"

        comparison = self.get_response(prompt)

        return {
            "topic": topic,
            "sources": sources,
            "comparison": comparison,
        }

    def _format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results for the LLM.

        Args:
            results: List of search results

        Returns:
            Formatted search results as a string
        """
        formatted = ""
        for i, result in enumerate(results, 1):
            formatted += f"Result {i}:\n"
            formatted += f"Title: {result.get('title', 'Untitled')}\n"
            formatted += f"URL: {result.get('url', 'No URL')}\n"
            formatted += f"Content: {result.get('content', 'No content')}\n\n"

        return formatted

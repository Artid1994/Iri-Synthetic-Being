"""
Tool Registry - Central dispatching for autonomous tool usage
Maps research intents to appropriate tools.
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

# Add Cerebellum to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))

from tools.web_search_tool import WebSearchTool
from tools.wikipedia_tool import WikipediaTool
from tools.pdf_doc_reader import PDFDocReader
from tools.python_sandbox import PythonSandbox
from tools.arxiv_research_tool import ArXivResearchTool
from tools.media_system_control import MediaSystemControl


class ToolRegistry:
    """Central registry for autonomous tool selection and dispatch."""
    
    def __init__(self):
        # Initialize all tools
        self.web_search = WebSearchTool()
        self.wikipedia = WikipediaTool()
        self.pdf_reader = PDFDocReader()
        self.python_sandbox = PythonSandbox()
        self.arxiv = ArXivResearchTool()
        self.system_control = MediaSystemControl()
        
        # Domain-to-tool mapping
        self.domain_tools = {
            'ai_ml': ['wikipedia', 'arxiv', 'web_search'],
            'mathematics': ['wikipedia', 'python_sandbox', 'web_search'],
            'computer_systems': ['wikipedia', 'web_search'],
            'programming': ['wikipedia', 'python_sandbox', 'web_search'],
            'physics': ['wikipedia', 'arxiv', 'web_search'],
            'general': ['wikipedia', 'web_search']
        }
    
    def select_tools_for_topic(self, topic: str, description: str = "") -> List[str]:
        """
        Select appropriate tools based on topic keywords.
        Returns list of tool names to use.
        """
        topic_lower = topic.lower()
        desc_lower = description.lower()
        text = topic_lower + " " + desc_lower
        
        # AI/ML domain
        if any(kw in text for kw in ['neural', 'llm', 'transformer', 'ai', 'machine learning']):
            return self.domain_tools['ai_ml']
        
        # Mathematics domain
        elif any(kw in text for kw in ['calculus', 'algebra', 'matrix', 'math', 'equation']):
            return self.domain_tools['mathematics']
        
        # Computer Systems domain
        elif any(kw in text for kw in ['operating system', 'process', 'computer', 'network']):
            return self.domain_tools['computer_systems']
        
        # Programming domain
        elif any(kw in text for kw in ['programming', 'python', 'code', 'algorithm']):
            return self.domain_tools['programming']
        
        # Physics domain
        elif any(kw in text for kw in ['physics', 'quantum', 'mechanics', 'relativity']):
            return self.domain_tools['physics']
        
        # Default: general tools
        else:
            return self.domain_tools['general']
    
    def research_with_tools(self, topic: str, description: str = "", max_facts: int = 5) -> List[Dict]:
        """
        Autonomous research using selected tools.
        Returns list of extracted facts.
        """
        tools_to_use = self.select_tools_for_topic(topic, description)
        facts = []
        
        # Wikipedia lookup (always try first for encyclopedic topics)
        if 'wikipedia' in tools_to_use:
            wiki_facts = self._research_wikipedia(topic, max_facts=2)
            facts.extend(wiki_facts)
        
        # ArXiv for academic topics
        if 'arxiv' in tools_to_use and len(facts) < max_facts:
            arxiv_facts = self._research_arxiv(topic, max_facts=2)
            facts.extend(arxiv_facts)
        
        # Web search as fallback
        if 'web_search' in tools_to_use and len(facts) < max_facts:
            web_facts = self._research_web(topic, max_facts=2)
            facts.extend(web_facts)
        
        # Python sandbox for code/math verification
        if 'python_sandbox' in tools_to_use and len(facts) < max_facts:
            # Can be extended to run example code
            pass
        
        return facts[:max_facts]
    
    def _research_wikipedia(self, topic: str, max_facts: int = 2) -> List[Dict]:
        """Extract facts from Wikipedia."""
        facts = []
        
        try:
            # Get article summary
            summary = self.wikipedia.get_summary(topic, sentences=3)
            if summary:
                # Split into sentences (simple)
                sentences = [s.strip() + '.' for s in summary.split('.') if s.strip()]
                
                for sentence in sentences[:max_facts]:
                    if len(sentence) > 20:  # Filter out too-short fragments
                        facts.append({
                            'text': sentence,
                            'source': 'wikipedia',
                            'confidence': 0.90
                        })
        except Exception:
            pass
        
        return facts
    
    def _research_arxiv(self, topic: str, max_facts: int = 2) -> List[Dict]:
        """Extract facts from ArXiv papers."""
        facts = []
        
        try:
            papers = self.arxiv.search(topic, max_results=2)
            for paper in papers[:max_facts]:
                if paper.get('summary'):
                    # Extract first sentence from abstract
                    first_sentence = paper['summary'].split('.')[0] + '.'
                    facts.append({
                        'text': first_sentence[:200],  # Truncate
                        'source': 'arxiv',
                        'confidence': 0.85,
                        'title': paper.get('title', '')
                    })
        except Exception:
            pass
        
        return facts
    
    def _research_web(self, topic: str, max_facts: int = 2) -> List[Dict]:
        """Extract facts from web search."""
        facts = []
        
        try:
            results = self.web_search.search(topic, max_results=3)
            for result in results[:max_facts]:
                if result.get('snippet'):
                    facts.append({
                        'text': result['snippet'],
                        'source': 'web_search',
                        'confidence': 0.75,
                        'url': result.get('url', '')
                    })
        except Exception:
            pass
        
        return facts

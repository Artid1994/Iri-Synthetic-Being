"""
ArXiv Research Tool - Academic paper search and extraction
Direct ArXiv API access for CS/Physics/Math research.
"""

import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional


class ArXivResearchTool:
    """ArXiv API tool for academic research papers."""
    
    def __init__(self):
        self.api_url = "http://export.arxiv.org/api/query"
        self.timeout = 15
    
    def search(self, query: str, max_results: int = 5, category: str = None) -> List[Dict]:
        """
        Search ArXiv papers.
        Category examples: 'cs.AI', 'cs.LG', 'math.CO', 'physics.comp-ph'
        """
        # Build search query
        search_query = f"all:{query}"
        if category:
            search_query = f"{search_query} AND cat:{category}"
        
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                xml_data = response.read()
            
            # Parse XML response
            root = ET.fromstring(xml_data)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            results = []
            for entry in root.findall('atom:entry', namespace):
                title = entry.find('atom:title', namespace)
                summary = entry.find('atom:summary', namespace)
                published = entry.find('atom:published', namespace)
                link = entry.find('atom:id', namespace)
                
                authors = []
                for author in entry.findall('atom:author', namespace):
                    name = author.find('atom:name', namespace)
                    if name is not None:
                        authors.append(name.text)
                
                results.append({
                    'title': title.text.strip() if title is not None else '',
                    'summary': summary.text.strip() if summary is not None else '',
                    'authors': authors,
                    'published': published.text if published is not None else '',
                    'url': link.text if link is not None else ''
                })
            
            return results
        
        except Exception:
            return []
    
    def get_paper_summary(self, arxiv_id: str) -> Optional[Dict]:
        """Get paper details by ArXiv ID (e.g., '2103.00020')."""
        params = {
            'id_list': arxiv_id,
            'max_results': 1
        }
        
        try:
            url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                xml_data = response.read()
            
            root = ET.fromstring(xml_data)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            entry = root.find('atom:entry', namespace)
            if entry is None:
                return None
            
            title = entry.find('atom:title', namespace)
            summary = entry.find('atom:summary', namespace)
            
            return {
                'title': title.text.strip() if title is not None else '',
                'summary': summary.text.strip() if summary is not None else ''
            }
        
        except Exception:
            return None

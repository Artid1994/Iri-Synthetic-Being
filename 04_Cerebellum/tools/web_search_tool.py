"""
Web Search Tool - Lightweight search without paid APIs
Uses DuckDuckGo HTML scraping as fallback.
"""

import re
import urllib.request
import urllib.parse
from typing import List, Dict, Optional


class WebSearchTool:
    """Lightweight web search tool using DuckDuckGo HTML."""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        self.timeout = 10
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search web using DuckDuckGo HTML interface.
        Returns list of {title, url, snippet} dicts.
        """
        try:
            # URL encode query
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            
            # Create request with user agent
            req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            
            # Fetch results
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                html = response.read().decode('utf-8')
            
            # Parse results (simple regex extraction)
            results = []
            
            # Extract result blocks
            result_pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>'
            snippet_pattern = r'<a class="result__snippet"[^>]*>([^<]+)</a>'
            
            titles = re.findall(result_pattern, html)
            snippets = re.findall(snippet_pattern, html)
            
            for i, (url, title) in enumerate(titles[:max_results]):
                snippet = snippets[i] if i < len(snippets) else ""
                results.append({
                    'title': title.strip(),
                    'url': url.strip(),
                    'snippet': snippet.strip()
                })
            
            return results
        
        except Exception as e:
            # Return empty on error (graceful fallback)
            return []
    
    def extract_text(self, url: str, max_chars: int = 2000) -> Optional[str]:
        """
        Extract plain text from URL (simple HTML stripping).
        Returns first max_chars characters.
        """
        try:
            req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            # Remove scripts and styles
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
            
            # Strip HTML tags
            text = re.sub(r'<[^>]+>', ' ', html)
            
            # Clean whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text[:max_chars]
        
        except Exception:
            return None

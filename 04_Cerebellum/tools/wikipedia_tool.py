"""
Wikipedia Tool - Direct MediaWiki API access
No external dependencies, uses standard library only.
"""

import json
import urllib.request
import urllib.parse
from typing import Optional, Dict


class WikipediaTool:
    """Wikipedia API tool for encyclopedic knowledge."""
    
    def __init__(self, lang: str = 'en'):
        self.lang = lang
        self.api_url = f"https://{lang}.wikipedia.org/w/api.php"
        self.timeout = 10
    
    def search(self, query: str, limit: int = 5) -> list:
        """Search Wikipedia articles."""
        params = {
            'action': 'opensearch',
            'search': query,
            'limit': limit,
            'format': 'json'
        }
        
        try:
            url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
            # 🟢 ปลดล็อกท่อเครือข่าย: ระบุหัวข้อสิทธิ์ User-Agent ตามกฎสากลของ MediaWiki API เพื่อไม่ให้โดนบล็อก
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'IriSyntheticBeing/1.0 (Contact: artid1994@debian)'}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read())
            
            # Format: [query, [titles], [descriptions], [urls]]
            if len(data) >= 4:
                results = []
                for i in range(len(data[1])):
                    results.append({
                        'title': data[1][i],
                        'description': data[2][i] if i < len(data[2]) else '',
                        'url': data[3][i] if i < len(data[3]) else ''
                    })
                return results
            return []
        
        except Exception:
            return []
    
    def get_summary(self, title: str, sentences: int = 3) -> Optional[str]:
        """Get article summary (first few sentences)."""
        params = {
            'action': 'query',
            'prop': 'extracts',
            'exintro': True,
            'exsentences': sentences,
            'explaintext': True,
            'titles': title,
            'format': 'json'
        }
        
        try:
            url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
            # 🟢 ปลดล็อกท่อเครือข่าย: ระบุหัวข้อสิทธิ์ User-Agent ตามกฎสากลของ MediaWiki API เพื่อไม่ให้โดนบล็อก
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'IriSyntheticBeing/1.0 (Contact: artid1994@debian)'}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read())
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if 'extract' in page_data:
                    return page_data['extract']
            
            return None
        
        except Exception:
            return None
    
    def get_content(self, title: str, max_chars: int = 5000) -> Optional[str]:
        """Get full article content (truncated to max_chars)."""
        params = {
            'action': 'query',
            'prop': 'extracts',
            'explaintext': True,
            'titles': title,
            'format': 'json'
        }
        
        try:
            url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
            # 🟢 ปลดล็อกท่อเครือข่าย: ระบุหัวข้อสิทธิ์ User-Agent ตามกฎสากลของ MediaWiki API เพื่อไม่ให้โดนบล็อก
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'IriSyntheticBeing/1.0 (Contact: artid1994@debian)'}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read())
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if 'extract' in page_data:
                    content = page_data['extract']
                    return content[:max_chars]
            
            return None
        
        except Exception:
            return None

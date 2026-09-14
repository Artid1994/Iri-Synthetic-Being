"""
Native Knowledge Response Module
Constructs responses from IRI's semantic memory without external AI
"""
from __future__ import annotations
from typing import Optional, List
from runtime.memory import Memory


class KnowledgeResponseBuilder:
    """
    Build responses from IRI's learned knowledge in semantic memory.
    
    Pure computational approach - no LLM/external AI.
    """
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def build_response(self, user_input: str, recalled: str) -> Optional[str]:
        """
        Construct response from semantic memory knowledge.
        
        Args:
            user_input: User's question
            recalled: Recalled information from memory
        
        Returns:
            Constructed response or None if no knowledge found
        """
        # Search semantic memory for relevant facts
        semantic_entries = self._search_semantic_memory(user_input)
        
        if not semantic_entries:
            return None
        
        # Extract answer from matched semantic entries
        answer = self._extract_answer(user_input, semantic_entries)
        
        return answer
    
    def _search_semantic_memory(self, query: str) -> List[str]:
        """Search semantic memory for entries matching query terms."""
        query_lower = query.lower()
        
        # Extract key terms from query (simple word tokenization)
        # Remove common question words
        stop_words = {'what', 'is', 'the', 'does', 'mean', 'how', 'why', 'where', 'when', 'who'}
        query_terms = [
            word.strip('?.!,') 
            for word in query_lower.split() 
            if word.strip('?.!,') not in stop_words and len(word) > 2
        ]
        
        if not query_terms:
            return []
        
        # Search semantic memory
        matches = []
        for entry in self.memory.state.semantic:
            entry_lower = entry.lower()
            # Check if any query term appears in semantic entry
            if any(term in entry_lower for term in query_terms):
                matches.append(entry)
        
        return matches
    
    def _extract_answer(self, query: str, semantic_entries: List[str]) -> Optional[str]:
        """
        Extract answer from semantic memory entries.
        
        Looks for patterns like:
        - "X means Y" -> extract Y
        - "X is Y" -> extract Y
        - "capital of X is Y" -> extract Y
        """
        query_lower = query.lower()
        
        # Pattern 1: "What does X mean?" queries (Thai -> English)
        if 'mean' in query_lower or 'means' in query_lower:
            return self._extract_meaning(query, semantic_entries)
        
        # Pattern 2: "How do you say X in Thai?" (English -> Thai)
        if ('say' in query_lower and 'thai' in query_lower) or \
           ('thai word' in query_lower):
            return self._extract_reverse_translation(query, semantic_entries)

        # Pattern 3: "What is X?" queries
        if 'what is' in query_lower or 'what\'s' in query_lower:
            return self._extract_definition(query, semantic_entries)
        
        # Pattern 4: Translation queries (contains Thai script)
        if self._contains_thai(query):
            return self._extract_translation(query, semantic_entries)
        
        # Default: Return first matching semantic entry
        if semantic_entries:
            return semantic_entries[0]
        
        return None
    
    def _extract_meaning(self, query: str, entries: List[str]) -> Optional[str]:
        """Extract meaning from 'X means Y' patterns."""
        for entry in entries:
            if ' means ' in entry.lower():
                # Split on 'means' and return the part after
                parts = entry.split(' means ', 1)
                if len(parts) == 2:
                    return parts[1].strip()
                    
            # Alternative: "Thai: X means Y"
            if 'thai:' in entry.lower() and ' means ' in entry.lower():
                parts = entry.lower().split(' means ', 1)
                if len(parts) == 2:
                    return parts[1].strip().capitalize()
        
        return None
    
    def _extract_definition(self, query: str, entries: List[str]) -> Optional[str]:
        """Extract definition from 'X is Y' patterns."""
        for entry in entries:
            if ' is ' in entry.lower():
                # Split on 'is' and return the part after
                parts = entry.split(' is ', 1)
                if len(parts) == 2:
                    answer = parts[1].strip()
                    # Remove trailing period if present
                    if answer.endswith('.'):
                        answer = answer[:-1]
                    return answer
        
        return None
    
    def _extract_translation(self, query: str, entries: List[str]) -> Optional[str]:
        """Extract English translation for Thai text."""
        # Extract Thai text from query
        thai_text = self._extract_thai_text(query)
        
        if not thai_text:
            return None
        
        # Search for translation in semantic entries
        for entry in entries:
            if thai_text in entry and ' means ' in entry.lower():
                parts = entry.split(' means ', 1)
                if len(parts) == 2:
                    return parts[1].strip()
        
        return None
    
    def _contains_thai(self, text: str) -> bool:
        """Check if text contains Thai script."""
        for char in text:
            if '\u0e00' <= char <= '\u0e7f':
                return True
        return False
    
    def _extract_thai_text(self, text: str) -> str:
        """Extract Thai text from mixed input."""
        thai_chars = []
        for char in text:
            if '\u0e00' <= char <= '\u0e7f' or char == ' ':
                thai_chars.append(char)
        return ''.join(thai_chars).strip()

    def _extract_reverse_translation(self, query: str, entries: List[str]) -> Optional[str]:
        """
        Extract Thai word from English meaning query.
        E.g., "How do you say water in Thai?" -> "น้ำ"
        """
        query_lower = query.lower()

        # Extract the English word being asked about
        # Remove question words and common phrases
        words_to_remove = [
            'how', 'do', 'you', 'say', 'in', 'thai', 'what', 'word', 'would',
            'use', 'to', 'express', 'for', 'the', 'is', 'a', 'an', '?', '.', ','
        ]

        query_words = query_lower.split()
        content_words = [
            w.strip('?.!,')
            for w in query_words
            if w.strip('?.!,') not in words_to_remove and len(w) > 2
        ]

        if not content_words:
            return None

        # Semantic equivalents for common concepts
        semantic_groups = {
            'gratitude': ['thank', 'thanks', 'gratitude', 'grateful'],
            'greeting': ['hello', 'hi', 'greet', 'greeting', 'salutation'],
            'affirmation': ['yes', 'affirmative', 'agree', 'affirmation'],
            'negation': ['no', 'negative', 'deny', 'negation'],
        }

        # Expand content words with semantic equivalents
        expanded_words = set(content_words)
        for word in content_words:
            for group_words in semantic_groups.values():
                if word in group_words:
                    expanded_words.update(group_words)

        # Look for entries where the English meaning matches
        best_match = None
        best_match_score = 0

        for entry in entries:
            if ' means ' in entry.lower():
                parts = entry.split(' means ')
                if len(parts) == 2:
                    thai_part = parts[0].strip()
                    english_part = parts[1].strip().lower()

                    # Count how many words match
                    match_score = sum(1 for word in expanded_words if word in english_part)

                    if match_score > best_match_score:
                        best_match_score = match_score
                        # Extract just the Thai word (remove "Thai: " prefix)
                        if thai_part.lower().startswith('thai:'):
                            best_match = thai_part[5:].strip()
                        else:
                            best_match = thai_part

        return best_match

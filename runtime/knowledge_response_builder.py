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
        # Check for temporal/recency queries first
        temporal_answer = self._check_temporal_context(user_input)
        if temporal_answer:
            return temporal_answer
        
        # Search semantic memory for relevant facts
        semantic_entries = self._search_semantic_memory(user_input)
        
        if not semantic_entries:
            return None
        
        # Extract answer from matched semantic entries
        answer = self._extract_answer(user_input, semantic_entries)
        
        return answer
    
    def _check_temporal_context(self, query: str) -> Optional[str]:
        """Check if query asks for recent/temporal context and prioritize working memory."""
        query_lower = query.lower()
        
        # Temporal keywords
        temporal_markers = [
            'recent', 'just', 'last', 'latest', 'most recent',
            'เมื่อกี้', 'ก่อนหน้า', 'ล่าสุด', 'ที่ผ่านมา'  # Thai: just now, before, latest, past
        ]
        
        is_temporal = any(marker in query_lower for marker in temporal_markers)
        
        if not is_temporal:
            return None
        
        # Prioritize working memory (most recent context)
        working = self.memory.state.working[-5:] if self.memory.state.working else []
        
        if not working:
            return None
        
        # Filter out queries/questions from working memory
        # Questions typically start with question words or end with '?'
        question_starters = ['what', 'how', 'when', 'where', 'why', 'who', 'which', 'อะไร', 'ยังไง', 'เมื่อไหร่']
        non_queries = [
            entry for entry in working
            if not any(entry.lower().strip().startswith(q) for q in question_starters)
            and not entry.strip().endswith('?')
        ]
        
        # Return most recent non-query working memory entry
        return non_queries[-1] if non_queries else None
    
    def _search_semantic_memory(self, query: str) -> List[str]:
        """Search semantic memory for entries matching query terms, prioritizing recent entries."""
        query_lower = query.lower()
        query_stripped = query.strip()
        
        # Check working memory first for recent context
        # Filter out the query itself to avoid self-matching
        working = [
            entry for entry in (self.memory.state.working[-5:] if self.memory.state.working else [])
            if entry.strip() != query_stripped
        ]
        
        # Detect temporal/meta queries (recent, just, latest, last, previous)
        temporal_markers = ['recent', 'just', 'latest', 'last', 'previous', 'เมื่อกี้', 'ล่าสุด']
        is_temporal = any(marker in query_lower for marker in temporal_markers)
        
        if is_temporal:
            # Return most recent non-query entries from working memory
            return [e for e in working if e.strip() != query_stripped][-3:] if working else []
        
        # Check if query is primarily Thai - if so, use different matching
        if self._is_thai_query(query):
            # For Thai queries, match by character overlap since Thai doesn't use spaces
            matches = []
            
            # Extract meaningful Thai character sequences (length 2+)
            # Remove question markers
            query_clean = query.replace('คืออะไร', '').replace('?', '').strip()
            
            # Search working memory
            for entry in reversed(working):
                if self._contains_thai(entry):
                    # Check for substring match or shared character sequences
                    if query_clean in entry or any(
                        query_clean[i:i+3] in entry 
                        for i in range(len(query_clean)-2)
                        if query_clean[i:i+3].strip()
                    ):
                        matches.append(entry)
            
            # Search semantic memory
            for entry in reversed(self.memory.state.semantic):
                if entry in matches:
                    continue
                if self._contains_thai(entry):
                    if query_clean in entry or any(
                        query_clean[i:i+3] in entry 
                        for i in range(len(query_clean)-2)
                        if query_clean[i:i+3].strip()
                    ):
                        matches.append(entry)
            
            return matches
        
        # English query processing
        # Extract key terms from query (simple word tokenization)
        # Remove common question words but keep single-letter terms for cases like "What is X?"
        stop_words = {'what', 'is', 'the', 'does', 'mean', 'how', 'why', 'where', 'when', 'who', 'you', 'should', 'know', 'can', 'could', 'would', 'a', 'an', 'of', 'to', 'in', 'on', 'at', 'for', 'was', 'are', 'be'}
        query_terms = [
            word.strip('?.!,') 
            for word in query_lower.split() 
            if word.strip('?.!,') not in stop_words and len(word.strip('?.!,')) >= 1  # Allow single chars
        ]
        
        # Also extract any Thai or special characters
        thai_parts = []
        for word in query.split():
            if self._contains_thai(word):
                thai_parts.append(word.strip('?.!,'))
        query_terms.extend(thai_parts)
        
        if not query_terms:
            # If no terms found, return recent context
            if working:
                return list(reversed(working[-3:]))
            return []
        
        # Search working memory first (recent context)
        matches = []
        for entry in reversed(working):  # Most recent first
            entry_lower = entry.lower()
            # Match if any term appears
            if any(term in entry_lower or term in entry for term in query_terms):
                matches.append(entry)
        
        # Then search semantic memory (older knowledge)
        for entry in reversed(self.memory.state.semantic):  # Recent first
            if entry in matches:  # Skip duplicates
                continue
            entry_lower = entry.lower()
            if any(term in entry_lower or term in entry for term in query_terms):
                matches.append(entry)
        
        return matches
    
    def _extract_answer(self, query: str, semantic_entries: List[str]) -> Optional[str]:
        """
        Extract answer from semantic memory entries.
        
        Looks for patterns like:
        - "X means Y" -> extract Y
        - "X is Y" -> extract Y
        - "capital of X is Y" -> extract Y
        - Thai patterns: "X คือ Y"
        """
        query_lower = query.lower()
        
        # Pattern -1: Temporal queries (most recent, just, latest, last)
        temporal_markers = ['recent', 'just', 'latest', 'last', 'previous', 'เมื่อกี้', 'ล่าสุด']
        is_temporal = any(marker in query_lower for marker in temporal_markers)
        if is_temporal and semantic_entries:
            # Return the most recent (last) entry for temporal queries
            return semantic_entries[-1]
        
        # Pattern 0: Thai queries (check first since Thai text has different structure)
        if self._is_thai_query(query):
            thai_answer = self._handle_thai_query(query, semantic_entries)
            if thai_answer:
                return thai_answer
        
        # Pattern 1: "What does X mean?" queries (Thai -> English)
        if 'mean' in query_lower or 'means' in query_lower:
            return self._extract_meaning(query, semantic_entries)
        
        # Pattern 2: "How do you say X in Thai?" (English -> Thai)
        # Also handles: "What would X say?", "Express X", "Show X", "word for X"
        if ('say' in query_lower and 'thai' in query_lower) or \
           ('thai word' in query_lower) or \
           ('would' in query_lower and 'thai' in query_lower) or \
           ('express' in query_lower) or \
           ('show' in query_lower and ('appreciation' in query_lower or 'gratitude' in query_lower)) or \
           ('called' in query_lower and 'thai' in query_lower) or \
           ('word' in query_lower and 'thai' in query_lower) or \
           ('written as' in query_lower and 'thai' in query_lower) or \
           ('using' in query_lower and 'thai' in query_lower):
            return self._extract_reverse_translation(query, semantic_entries)

        # Pattern 3: "What is X?" queries
        if 'what is' in query_lower or 'what\'s' in query_lower:
            return self._extract_definition(query, semantic_entries)
        
        # Pattern 4: Translation queries (contains Thai script but not full Thai query)
        if self._contains_thai(query) and not self._is_thai_query(query):
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
        """Extract English translation for Thai text or handle Thai-to-Thai queries."""
        # Extract Thai text from query
        thai_text = self._extract_thai_text(query)
        
        if not thai_text:
            # Check if entire query is Thai (Thai-to-Thai conversation)
            if self._is_thai_query(query):
                return self._handle_thai_query(query, entries)
            return None
        
        # Search for translation in semantic entries
        for entry in entries:
            if thai_text in entry and ' means ' in entry.lower():
                parts = entry.split(' means ', 1)
                if len(parts) == 2:
                    return parts[1].strip()
            # Also check for Thai definition patterns
            if thai_text in entry and ' คือ ' in entry:
                parts = entry.split(' คือ ', 1)
                if len(parts) == 2:
                    return parts[1].strip()
        
        return None
    
    def _is_thai_query(self, text: str) -> bool:
        """Check if text is primarily Thai script."""
        thai_chars = sum(1 for c in text if '\u0e00' <= c <= '\u0e7f')
        total_chars = sum(1 for c in text if c.isalpha())
        return total_chars > 0 and thai_chars / total_chars > 0.5
    
    def _handle_thai_query(self, query: str, entries: List[str]) -> Optional[str]:
        """Handle Thai-to-Thai queries (e.g., เมืองหลวงของไทยคืออะไร)."""
        query_lower = query.lower()
        
        # Thai query patterns
        if 'คืออะไร' in query or 'คือ' in query:  # "what is" in Thai
            # Extract keywords from the question
            # Remove question words
            query_clean = query.replace('คืออะไร', '').replace('คือ', '').strip()
            query_words = query_clean.split()
            
            # Search entries for matching Thai content
            for entry in entries:
                # Look for Thai definitions: X คือ Y
                if ' คือ ' in entry:
                    parts = entry.split(' คือ ')
                    if len(parts) == 2:
                        subject = parts[0].strip()
                        answer = parts[1].strip()
                        
                        # Check if any query word appears in subject or answer
                        for word in query_words:
                            if word and len(word) > 1:
                                if word in subject or word in answer:
                                    return answer
                
                # Also handle English patterns with Thai: "capital" mentioned
                if self._contains_thai(entry):
                    # Check for English keywords in query that might match
                    if any(keyword in query_lower for keyword in ['capital', 'เมือง', 'หลวง', 'ประเทศ', 'ไทย']):
                        if ' คือ ' in entry:
                            parts = entry.split(' คือ ')
                            if len(parts) == 2:
                                return parts[1].strip()
                        elif ' means ' in entry.lower():
                            # Handle mixed Thai-English: "X means Y"
                            parts = entry.split(' means ', 1)
                            if len(parts) == 2 and self._contains_thai(parts[0]):
                                # If query mentions the concept, return Thai word
                                english_part = parts[1].strip().lower()
                                if any(word in english_part for word in query_words):
                                    return parts[0].strip()
        
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
            'use', 'to', 'express', 'for', 'the', 'is', 'a', 'an', '?', '.', ',',
            'show', 'using', 'phrase', 'speaker', 'language', 'represents',
            'should', 'know', 'called', 'written', 'script', 'when', 'used',
            'daily', 'essential', 'life', 'tastes', 'gesture', 'staple'
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
            'gratitude': ['thank', 'thanks', 'gratitude', 'grateful', 'appreciation', 'appreciate', 'thankfulness'],
            'greeting': ['hello', 'hi', 'greet', 'greeting', 'salutation', 'gesture'],
            'affirmation': ['yes', 'affirmative', 'agree', 'affirmation'],
            'negation': ['no', 'negative', 'deny', 'negation'],
            'water': ['water', 'beverage', 'drink', 'liquid', 'thirsty', 'hydrate'],
            'rice': ['rice', 'grain', 'food', 'staple', 'eaten', 'meal'],
            'delicious': ['delicious', 'tasty', 'good', 'taste', 'yummy', 'flavor'],
        }

        # Expand content words with semantic equivalents
        expanded_words = set(content_words)
        for word in content_words:
            for group_words in semantic_groups.values():
                if word in group_words:
                    expanded_words.update(group_words)
                    break  # Found group, no need to check others

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

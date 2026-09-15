#!/usr/bin/env python3
"""
Semantic Knowledge Store for AE01M
Stores and retrieves structured semantic facts with question-answering capability.
"""
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class SemanticKnowledgeStore:
    """Store and query semantic facts with structured question answering."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent / "semantic_facts.json"
        self.facts = []
        self.load()
    
    def add_fact(self, subject: str, predicate: str, object_: str, context: str = ""):
        """Add a new semantic fact."""
        fact = {
            'subject': subject,
            'predicate': predicate,
            'object': object_,
            'context': context,
            'learned_at': datetime.now().isoformat()
        }
        self.facts.append(fact)
        self.save()
    
    def add_facts(self, facts: List[Dict]):
        """Add multiple semantic facts."""
        for fact in facts:
            if isinstance(fact, dict):
                self.facts.append(fact)
            else:
                # Handle SemanticFact objects
                self.facts.append(fact.to_dict())
        self.save()
    
    def save(self):
        """Persist facts to disk."""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.facts, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def load(self):
        """Load facts from disk."""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.facts = json.load(f)
        except Exception:
            self.facts = []
    
    def query(self, question: str) -> str:
        """
        Answer a question using stored semantic facts.
        Returns a natural language answer or empty string if no relevant fact found.
        """
        question_lower = question.lower()
        
        # Extract key entities from question
        entities = self._extract_question_entities(question)
        
        if not entities:
            return ""
        
        # Search for relevant facts
        relevant_facts = []
        
        for fact in self.facts:
            subject_lower = fact['subject'].lower()
            object_lower = fact['object'].lower()
            
            # Check if question entities match fact entities
            for entity in entities:
                entity_lower = entity.lower()
                if (entity_lower in subject_lower or 
                    entity_lower in object_lower or
                    subject_lower in entity_lower or
                    object_lower in entity_lower):
                    relevant_facts.append(fact)
                    break
        
        if not relevant_facts:
            return ""
        
        # Determine question type and generate appropriate answer
        return self._generate_answer(question, relevant_facts)
    
    def _extract_question_entities(self, question: str) -> List[str]:
        """Extract key entities from a question."""
        entities = []
        
        # Thai question patterns
        # "X คืออะไร" (What is X?)
        match = re.search(r'(.+?)\s*คืออะไร', question)
        if match:
            entities.append(match.group(1).strip())
        
        # "X ชอบทำอะไร" (What does X like to do?)
        match = re.search(r'(.+?)\s*ชอบ(?:ทำ)?อะไร', question)
        if match:
            entities.append(match.group(1).strip())
        
        # "X อาศัยอยู่ที่ไหน" (Where does X live?)
        match = re.search(r'(.+?)\s*อาศัยอยู่(?:ที่)?ไหน', question)
        if match:
            entities.append(match.group(1).strip())
        
        # "สัตว์ที่...ชื่ออะไร" (What is the name of the animal that...)
        match = re.search(r'(?:สัตว์|สิ่ง)(?:ที่|ซึ่ง)?.*?ชื่ออะไร', question)
        if match:
            # Extract descriptive terms
            inner_match = re.search(r'(?:สัตว์|สิ่ง)(?:ที่|ซึ่ง)?(.+?)ชื่ออะไร', question)
            if inner_match:
                desc = inner_match.group(1).strip()
                # Look for key descriptive verbs
                for keyword in ['สอน', 'บอก', 'เพิ่ง', 'เรียน']:
                    if keyword in desc:
                        entities.append('__recently_taught__')
                        break
        
        # English question patterns
        # "What is X?"
        match = re.search(r'what\s+is\s+(.+?)[\?]?$', question, re.IGNORECASE)
        if match:
            entities.append(match.group(1).strip())
        
        # "Where does X live?"
        match = re.search(r'where\s+(?:does|do)\s+(.+?)\s+live', question, re.IGNORECASE)
        if match:
            entities.append(match.group(1).strip())
        
        # If no pattern matched, extract quoted or capitalized words
        if not entities:
            # Extract words in quotes
            quoted = re.findall(r'["\'](.+?)["\']', question)
            entities.extend(quoted)
            
            # Extract Thai words (any Thai characters form an entity)
            thai_words = re.findall(r'[\u0e00-\u0e7f]+', question)
            entities.extend([w for w in thai_words if len(w) > 1])
        
        return entities
    
    def _generate_answer(self, question: str, relevant_facts: List[Dict]) -> str:
        """Generate a natural language answer from relevant facts."""
        question_lower = question.lower()
        
        # Determine question type
        
        # Thai: "X คืออะไร" (What is X?)
        if 'คืออะไร' in question or 'คืออะไร' in question:
            # Extract the entity being asked about
            match = re.search(r'(.+?)\s*คืออะไร', question)
            if match:
                entity = match.group(1).strip().lower()
                
                # Prioritize definition facts where subject matches the entity
                definition_facts = [
                    f for f in relevant_facts 
                    if f['predicate'] == 'คือ' and f['subject'].lower().strip() == entity
                ]
                
                # Return the longest/most descriptive definition
                if definition_facts:
                    best_fact = max(definition_facts, key=lambda f: len(f['object']))
                    return f"{best_fact['subject']}คือ{best_fact['object']}ครับ"
            
            # Fallback to any fact with 'คือ' predicate
            for fact in relevant_facts:
                if fact['predicate'] == 'คือ':
                    return f"{fact['subject']}คือ{fact['object']}ครับ"
        
        # Thai: "X ชอบทำอะไร" (What does X like to do?)
        if 'ชอบ' in question and 'อะไร' in question:
            for fact in relevant_facts:
                if 'ชอบ' in fact['predicate'] or 'ชอบ' in fact['object']:
                    return f"{fact['subject']}{fact['predicate']}{fact['object']}ครับ"
        
        # Thai: "X อาศัยอยู่ที่ไหน" (Where does X live?)
        if 'อาศัย' in question or 'นอน' in question:
            for fact in relevant_facts:
                if 'อาศัย' in fact['predicate'] or 'นอน' in fact['predicate']:
                    return f"{fact['subject']}{fact['predicate']}{fact['object']}ครับ"
        
        # Thai: "สัตว์ที่เพิ่งสอนชื่ออะไร" (What's the name of the animal I just taught?)
        if 'ชื่ออะไร' in question and ('สอน' in question or 'เพิ่ง' in question):
            # Return most recently learned named entity
            for fact in reversed(relevant_facts):
                if fact['predicate'] == 'ชื่อคือ':
                    return f"ชื่อ{fact['object']}ครับ"
                elif fact['predicate'] == 'คือ' and 'ชื่อ' in fact['subject']:
                    return f"ชื่อ{fact['object']}ครับ"
        
        # English: "What is X?"
        if 'what is' in question_lower:
            for fact in relevant_facts:
                if fact['predicate'] in ['is', 'คือ']:
                    return f"{fact['subject']} is {fact['object']}"
        
        # Default: return the most relevant fact
        if relevant_facts:
            fact = relevant_facts[0]
            return f"{fact['subject']}{fact['predicate']}{fact['object']}ครับ"
        
        return ""
    
    def get_recent_facts(self, limit: int = 10) -> List[Dict]:
        """Get most recently learned facts."""
        return list(reversed(self.facts[-limit:]))
    
    def clear(self):
        """Clear all stored facts (for testing)."""
        self.facts = []
        self.save()


if __name__ == "__main__":
    # Test semantic knowledge store
    store = SemanticKnowledgeStore(Path("/tmp/test_semantic.json"))
    store.clear()
    
    # Add test facts
    store.add_fact("ลูม่า", "คือ", "สัตว์สมมติ")
    store.add_fact("ลูม่า", "ชอบนอนบน", "ต้นไม้ตอนกลางวัน")
    store.add_fact("ลูม่า", "ออกหา", "อาหารในเวลากลางคืน")
    
    # Test queries
    questions = [
        "ลูม่าคืออะไร",
        "ลูม่าชอบทำอะไรตอนกลางวัน",
        "สัตว์ที่ฉันเพิ่งสอนเธอชื่ออะไร"
    ]
    
    for q in questions:
        answer = store.query(q)
        print(f"Q: {q}")
        print(f"A: {answer}\n")

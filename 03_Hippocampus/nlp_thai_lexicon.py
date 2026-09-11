#!/usr/bin/env python3
"""
Thai NLP Lexicon Manager
Provides fast entity recognition and lexicon lookup for Thai language processing.
Uses PyThaiNLP lexicon-thai and Thai-NER datasets.
"""
from pathlib import Path
from typing import List, Dict, Set, Optional
import re


class ThaiLexicon:
    """Thai lexicon and entity recognition manager."""
    
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            base_path = Path(__file__).parent / "knowledge_base" / "nlp_thai"
        
        self.base_path = Path(base_path)
        self.lexicon_path = self.base_path / "lexicon-thai"
        self.ner_path = self.base_path / "thai-ner"
        
        # Cached lexicons
        self._female_names: Optional[Set[str]] = None
        self._male_names: Optional[Set[str]] = None
        self._abbreviations: Optional[Dict[str, str]] = None
        self._action_verbs: Optional[Set[str]] = None
        
    def load_female_names(self) -> Set[str]:
        """Load Thai female names."""
        if self._female_names is None:
            path = self.lexicon_path / "thai-name" / "female.txt"
            if path.exists():
                self._female_names = set(path.read_text(encoding="utf-8").strip().split("\n"))
            else:
                self._female_names = set()
        return self._female_names
    
    def load_male_names(self) -> Set[str]:
        """Load Thai male names."""
        if self._male_names is None:
            path = self.lexicon_path / "thai-name" / "man.txt"
            if path.exists():
                self._male_names = set(path.read_text(encoding="utf-8").strip().split("\n"))
            else:
                self._male_names = set()
        return self._male_names
    
    def load_abbreviations(self) -> Dict[str, str]:
        """Load Thai abbreviations."""
        if self._abbreviations is None:
            path = self.lexicon_path / "thai-abbreviation" / "data.csv"
            self._abbreviations = {}
            if path.exists():
                lines = path.read_text(encoding="utf-8").strip().split("\n")
                for line in lines[1:]:  # Skip header
                    parts = line.split(",")
                    if len(parts) >= 2:
                        abbr = parts[0].strip()
                        full = parts[1].strip()
                        self._abbreviations[abbr] = full
        return self._abbreviations
    
    def is_person_name(self, token: str) -> bool:
        """Check if token is a Thai person name."""
        female_names = self.load_female_names()
        male_names = self.load_male_names()
        return token in female_names or token in male_names
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from Thai text.
        Returns dict with entity types: person, location, organization, etc.
        """
        entities = {
            "person": [],
            "action": [],
            "object": [],
            "unknown": []
        }
        
        # Simple tokenization by spaces (Thai text should be pre-segmented)
        tokens = text.split()
        
        for token in tokens:
            # Check if person name
            if self.is_person_name(token):
                entities["person"].append(token)
            # Check if action verb (Thai verbs often start with specific characters)
            elif self._is_action_verb(token):
                entities["action"].append(token)
            else:
                entities["object"].append(token)
        
        return entities
    
    def _is_action_verb(self, token: str) -> bool:
        """
        Detect Thai action verbs using simple heuristics.
        Common Thai verb prefixes: ก, ต, ป, ม, ร, ส, etc.
        """
        if not token:
            return False
        
        # Common Thai action verbs for command recognition
        action_verbs = {
            "เปิด", "ปิด", "เริ่ม", "หยุด", "แสดง", "ค้นหา", "บันทึก", "ลบ",
            "สร้าง", "แก้ไข", "เปลี่ยน", "ตรวจสอบ", "วิเคราะห์", "รายงาน",
            "ส่ง", "รับ", "อ่าน", "เขียน", "พูด", "ฟัง", "ดู", "เล่น",
            "เรียน", "สอน", "ทำงาน", "พัก", "นอน", "ตื่น", "กิน", "ดื่ม"
        }
        
        return token in action_verbs
    
    def expand_abbreviation(self, text: str) -> str:
        """Expand Thai abbreviations in text."""
        abbreviations = self.load_abbreviations()
        for abbr, full in abbreviations.items():
            text = text.replace(abbr, full)
        return text
    
    def extract_intent(self, text: str) -> Dict[str, any]:
        """
        Extract intent from Thai text without LLM.
        Returns: {
            "action": str,
            "target": str,
            "entities": dict,
            "confidence": float
        }
        """
        # Expand abbreviations first
        expanded_text = self.expand_abbreviation(text)
        
        # Extract entities
        entities = self.extract_entities(expanded_text)
        
        # Determine primary action
        action = entities["action"][0] if entities["action"] else "unknown"
        
        # Determine target (first non-action entity)
        target = None
        if entities["object"]:
            target = entities["object"][0]
        elif entities["person"]:
            target = entities["person"][0]
        
        # Calculate confidence based on entity coverage
        total_tokens = len(expanded_text.split())
        recognized_tokens = sum(len(v) for v in entities.values())
        confidence = recognized_tokens / total_tokens if total_tokens > 0 else 0.0
        
        return {
            "action": action,
            "target": target,
            "entities": entities,
            "confidence": confidence,
            "expanded_text": expanded_text
        }


# Singleton instance
_lexicon_instance: Optional[ThaiLexicon] = None


def get_thai_lexicon() -> ThaiLexicon:
    """Get singleton Thai lexicon instance."""
    global _lexicon_instance
    if _lexicon_instance is None:
        _lexicon_instance = ThaiLexicon()
    return _lexicon_instance


if __name__ == "__main__":
    # Test the lexicon
    lexicon = ThaiLexicon()
    
    print("=== Thai NLP Lexicon Test ===")
    print(f"Lexicon path: {lexicon.lexicon_path}")
    print(f"NER path: {lexicon.ner_path}")
    
    # Test name recognition
    female_names = lexicon.load_female_names()
    male_names = lexicon.load_male_names()
    print(f"\nLoaded {len(female_names)} female names")
    print(f"Loaded {len(male_names)} male names")
    print(f"Sample female names: {list(female_names)[:5]}")
    print(f"Sample male names: {list(male_names)[:5]}")
    
    # Test abbreviations
    abbr = lexicon.load_abbreviations()
    print(f"\nLoaded {len(abbr)} abbreviations")
    
    # Test intent extraction
    test_text = "เปิด ไฟ ห้องนอน"
    intent = lexicon.extract_intent(test_text)
    print(f"\nTest text: '{test_text}'")
    print(f"Extracted intent: {intent}")

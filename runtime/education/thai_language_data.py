"""
Thai Language Curriculum Data Loader
Loads authoritative Thai linguistic data from JSON files
"""
import json
from pathlib import Path
from typing import Dict, List, Any


class ThaiLanguageData:
    """Loads and provides Thai language data."""
    
    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        
        self.data_dir = Path(data_dir)
        self._consonants = None
        self._vowel_orthography = None
        self._vowel_phonology = None
        self._tones = None
    
    @property
    def consonants(self) -> List[Dict[str, Any]]:
        """Load consonant data."""
        if self._consonants is None:
            consonants_file = self.data_dir / "consonants.json"
            data = json.loads(consonants_file.read_text(encoding='utf-8'))
            self._consonants = data['consonants']
        return self._consonants
    
    @property
    def vowels(self) -> List[Dict[str, Any]]:
        """Load vowel orthography data (spelling forms)."""
        if self._vowel_orthography is None:
            # Try new file first, fall back to old name for compatibility
            vowel_file = self.data_dir / "vowel_orthography.json"
            if not vowel_file.exists():
                vowel_file = self.data_dir / "vowels.json"
            
            data = json.loads(vowel_file.read_text(encoding='utf-8'))
            self._vowel_orthography = data['vowels']
        return self._vowel_orthography
    
    @property
    def vowel_orthography(self) -> List[Dict[str, Any]]:
        """Load vowel orthography data (explicit name)."""
        return self.vowels
    
    @property
    def vowel_phonology(self) -> Dict[str, Any]:
        """Load vowel phonology data (sound units)."""
        if self._vowel_phonology is None:
            phonology_file = self.data_dir / "vowel_phonology.json"
            self._vowel_phonology = json.loads(phonology_file.read_text(encoding='utf-8'))
        return self._vowel_phonology
    
    @property
    def tones(self) -> Dict[str, Any]:
        """Load tone data."""
        if self._tones is None:
            tones_file = self.data_dir / "tones.json"
            self._tones = json.loads(tones_file.read_text(encoding='utf-8'))
        return self._tones
    
    def get_consonants_by_class(self, consonant_class: str, include_obsolete: bool = False) -> List[Dict[str, Any]]:
        """
        Get consonants filtered by class (low/mid/high).
        
        Args:
            consonant_class: 'low', 'mid', or 'high'
            include_obsolete: If True, include obsolete consonants (ฃ, ฅ)
        
        Returns:
            List of consonant dictionaries
        """
        consonants = [c for c in self.consonants if c['class'] == consonant_class]
        
        if not include_obsolete:
            consonants = [c for c in consonants if not c.get('obsolete', False)]
        
        return consonants
    
    def get_consonant(self, char: str) -> Dict[str, Any]:
        """Get consonant data by character."""
        for c in self.consonants:
            if c['char'] == char:
                return c
        raise ValueError(f"Consonant not found: {char}")
    
    def get_vowel(self, form: str) -> Dict[str, Any]:
        """Get vowel orthography data by form."""
        for v in self.vowels:
            if v['form'] == form:
                return v
        raise ValueError(f"Vowel not found: {form}")

"""
Thai Tone Calculation Algorithm
Deterministic tone assignment from orthography
"""
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class SyllableAnalysis:
    """Analysis of a Thai syllable for tone calculation."""
    initial_consonant: str
    consonant_class: str  # 'low', 'mid', 'high'
    vowel: str
    vowel_length: str  # 'short', 'long'
    final_consonant: Optional[str]
    tone_mark: Optional[str]  # '◌่', '◌้', '◌๊', '◌๋', or None
    is_live: bool  # True = live syllable, False = dead syllable
    effective_class: str  # After ห/อ leading modification


class ThaiToneCalculator:
    """
    Calculates Thai tone from orthographic syllable components.
    
    Based on authoritative Thai phonology rules:
    - Consonant class (low/mid/high)
    - Syllable type (live/dead)
    - Vowel length (short/long)
    - Tone mark (if present)
    - Leading ห/อ modification
    """
    
    # Tone mark to name mapping
    TONE_MARKS = {
        '่': 'mai_ek',
        '้': 'mai_tho',
        '๊': 'mai_tri',
        '๋': 'mai_chattawa',
    }
    
    # Sonorant finals (make syllable live)
    SONORANTS = {'ง', 'น', 'ม', 'ย', 'ร', 'ล', 'ว', 'ญ', 'ณ', 'ฬ'}
    
    # Stop finals (contribute to dead syllable)
    STOPS = {'ก', 'ข', 'ค', 'จ', 'ช', 'ซ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'บ', 'ป', 'พ', 'ฟ', 'ภ', 'ศ', 'ษ', 'ส'}
    
    def __init__(self, consonant_data: Dict, vowel_data: Dict, tone_rules: Dict):
        """
        Initialize with linguistic data.
        
        Args:
            consonant_data: Consonant class information
            vowel_data: Vowel length information
            tone_rules: Complete tone rule tables
        """
        self.consonant_data = consonant_data
        self.vowel_data = vowel_data
        self.tone_rules = tone_rules
    
    def determine_syllable_type(
        self,
        vowel_length: str,
        final_consonant: Optional[str]
    ) -> bool:
        """
        Determine if syllable is live or dead.
        
        Args:
            vowel_length: 'short' or 'long'
            final_consonant: Final consonant character, or None
        
        Returns:
            True if live syllable, False if dead syllable
        
        Rules:
            LIVE syllable:
            - Long vowel + no final
            - Long vowel + any final
            - Short vowel + sonorant final
            
            DEAD syllable:
            - Short vowel + stop final
            - Short vowel + no final (rare, only ◌ะ)
        """
        # No final consonant
        if final_consonant is None:
            return vowel_length == 'long'
        
        # Has final consonant
        if final_consonant in self.SONORANTS:
            return True  # Always live with sonorant
        elif final_consonant in self.STOPS:
            return vowel_length == 'long'  # Live if long vowel, dead if short
        else:
            # Unknown final, assume live for safety
            return True
    
    def apply_leading_h_modification(
        self,
        initial: str,
        consonant_class: str,
        leading_h: bool = False
    ) -> str:
        """
        Apply ห leading modification rule.
        
        If ห precedes a low-class sonorant, effective class becomes high.
        
        Args:
            initial: Initial consonant
            consonant_class: Original class of initial
            leading_h: Whether ห precedes this consonant
        
        Returns:
            Effective consonant class after modification
        """
        if leading_h and consonant_class == 'low' and initial in self.SONORANTS:
            return 'high'
        return consonant_class
    
    def calculate_tone(self, analysis: SyllableAnalysis) -> int:
        """
        Calculate tone number (0-4) from syllable analysis.
        
        Args:
            analysis: Complete syllable analysis
        
        Returns:
            Tone number: 0=mid, 1=low, 2=falling, 3=high, 4=rising
        
        Raises:
            ValueError: If tone cannot be determined (invalid combination)
        """
        effective_class = analysis.effective_class
        tone_mark_name = self.TONE_MARKS.get(analysis.tone_mark) if analysis.tone_mark else 'no_mark'
        
        if analysis.is_live:
            # Live syllable rules
            rules = self.tone_rules['tone_rules']['live_syllable']
            
            if effective_class == 'mid':
                class_rules = rules['mid_class']
            elif effective_class == 'high':
                class_rules = rules['high_class']
            elif effective_class == 'low':
                class_rules = rules['low_class']
            else:
                raise ValueError(f"Unknown consonant class: {effective_class}")
            
            tone = class_rules.get(tone_mark_name)
            
            if tone is None or tone == "not_used":
                raise ValueError(
                    f"Tone mark {analysis.tone_mark} ({tone_mark_name}) not valid with {effective_class} class in live syllable"
                )
            
            return int(tone)
        
        else:
            # Dead syllable rules
            rules = self.tone_rules['tone_rules']['dead_syllable']
            
            # Dead syllables don't use tone marks (except in rare cases)
            if analysis.tone_mark:
                raise ValueError("Dead syllables typically do not have tone marks")
            
            if analysis.vowel_length == 'short':
                vowel_rules = rules['short_vowel']
            else:
                vowel_rules = rules['long_vowel']
            
            if effective_class == 'mid':
                return int(vowel_rules['mid_class'])
            elif effective_class == 'high':
                return int(vowel_rules['high_class'])
            elif effective_class == 'low':
                return int(vowel_rules['low_class'])
            else:
                raise ValueError(f"Unknown consonant class: {effective_class}")
    
    def get_tone_name(self, tone_number: int) -> str:
        """
        Get tone name from tone number.
        
        Args:
            tone_number: 0-4
        
        Returns:
            Tone name in English
        """
        tone_names = {
            0: "mid tone",
            1: "low tone",
            2: "falling tone",
            3: "high tone",
            4: "rising tone"
        }
        return tone_names.get(tone_number, "unknown")

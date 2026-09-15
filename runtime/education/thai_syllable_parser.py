"""
Thai Syllable Parser
Parses Thai orthographic text into structured syllable components

Architecture:
    Orthographic Text → Token Stream → Syllable Components → SyllableAnalysis

Rules:
    - Explicit pattern matching (no guessing)
    - Vowel position detection (leading/above/below/trailing)
    - Consonant cluster identification
    - Tone mark extraction
    - Leading ห/อ detection
    - Live/dead syllable classification
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple
import re

from runtime.education.thai_tone_calculator import SyllableAnalysis, ThaiToneCalculator


@dataclass
class ParseError:
    """Represents an ambiguity or error in parsing."""
    position: int
    character: str
    reason: str
    context: str


class ThaiSyllableParser:
    """
    Parses Thai orthographic syllables into structured components.
    
    Uses explicit pattern matching - ambiguous patterns are flagged,
    never silently guessed.
    """
    
    # Thai character ranges
    THAI_CONSONANTS = set('กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ')
    THAI_VOWELS_LEADING = set('เแโใไ')  # Written before consonant
    THAI_VOWELS_ABOVE = set('◌ิ◌ี◌ึ◌ื◌ั◌็ิีึืั็')  # Written above
    THAI_VOWELS_BELOW = set('◌ุ◌ูุู')  # Written below
    THAI_VOWELS_TRAILING = set('าะอๅ')  # Written after consonant
    THAI_TONE_MARKS = set('่้๊๋')  # Tone marks
    THAI_SPECIAL = set('์ๆฯ')  # Silent letter, repetition, etc.
    
    # Sonorant consonants (for live/dead determination)
    SONORANTS = set('งญณนมยรลวฬ')
    
    # Stop consonants (for live/dead determination)
    STOPS = set('กขฃคฅฆจฉชซฌฎฏฐฑฒดตถทธบปผฝพฟภศษส')
    
    # Valid initial clusters
    VALID_CLUSTERS = {
        'กร', 'กล', 'กว',
        'ขร', 'ขล', 'ขว',
        'คร', 'คล', 'คว',
        'ตร', 'ตล',
        'ปร', 'ปล',
        'พร', 'พล',
        'ทร',  # Pronounced /s/, not /tʰr/
    }
    
    def __init__(self, consonant_data: dict, vowel_data: dict, tone_data: dict):
        """
        Initialize parser with linguistic data.
        
        Args:
            consonant_data: Consonant class information
            vowel_data: Vowel orthography data
            tone_data: Tone rules
        """
        self.consonant_data = consonant_data
        self.vowel_data = vowel_data
        self.tone_data = tone_data
        
        # Build consonant class lookup
        self.consonant_classes = {}
        for c in consonant_data['consonants']:
            self.consonant_classes[c['char']] = c['class']
        
        # Build vowel length lookup
        self.vowel_lengths = {}
        for v in vowel_data['vowels']:
            # Map vowel form to length
            form = v['form'].replace('◌', '')  # Remove placeholder
            self.vowel_lengths[form] = v['length']
    
    def parse_syllable(self, text: str) -> Tuple[Optional[SyllableAnalysis], List[ParseError]]:
        """
        Parse a single Thai syllable from orthographic text.
        
        Args:
            text: Thai syllable in orthographic form
        
        Returns:
            Tuple of (SyllableAnalysis or None, list of ParseError)
        
        The parser attempts to extract all components. If critical
        components are missing or ambiguous, returns None with errors.
        """
        errors = []
        
        if not text or not text.strip():
            errors.append(ParseError(0, '', 'Empty input', text))
            return None, errors
        
        text = text.strip()
        
        # Step 1: Detect leading vowels (เ แ โ ใ ไ)
        leading_vowel = ''
        if text[0] in self.THAI_VOWELS_LEADING:
            leading_vowel = text[0]
            text = text[1:]
        
        # Step 2: Detect leading ห or อ modification
        leading_h = False
        leading_o = False
        
        if len(text) >= 2:
            # IMPORTANT: Check leading ห + sonorant BEFORE cluster detection
            # ห + sonorant is NOT a cluster, it's a tone modification
            if text[0] == 'ห' and text[1] in self.SONORANTS:
                leading_h = True
                text = text[1:]  # Remove ห, keep sonorant
            elif text[0] == 'อ' and text[1] in self.THAI_CONSONANTS:
                leading_o = True
                text = text[1:]  # Remove อ, keep consonant
        
        # Step 3: Extract initial consonant(s)
        initial_consonant = ''
        consonant_cluster = ''
        
        if not text:
            errors.append(ParseError(0, '', 'No consonant after leading element', leading_vowel))
            return None, errors
        
        if text[0] not in self.THAI_CONSONANTS:
            errors.append(ParseError(0, text[0], 'Expected consonant', text))
            return None, errors
        
        initial_consonant = text[0]
        text = text[1:]
        
        # Check for cluster (second consonant)
        # IMPORTANT: This runs AFTER leading ห detection, so หม won't be confused as cluster
        if text and text[0] in self.THAI_CONSONANTS:
            potential_cluster = initial_consonant + text[0]
            if potential_cluster in self.VALID_CLUSTERS:
                consonant_cluster = potential_cluster
                text = text[1:]
            # If not valid cluster, second consonant is likely syllable boundary
        
        # Step 4: Extract vowel (above/below markers, trailing vowels)
        vowel_above = ''
        vowel_below = ''
        vowel_trailing = ''
        tone_mark = ''
        
        # Scan for above/below vowels and tone marks
        i = 0
        while i < len(text):
            char = text[i]
            
            if char in self.THAI_VOWELS_ABOVE or char in 'ิีึืั็':
                vowel_above += char
            elif char in self.THAI_VOWELS_BELOW or char in 'ุู':
                vowel_below += char
            elif char in self.THAI_TONE_MARKS:
                tone_mark = char
            elif char in 'าะอๅ':  # Trailing vowels
                vowel_trailing += char
            elif char == '์':  # Silent letter marker (thanthakhat)
                # Skip the marker - will handle silent finals separately
                pass
            elif char in self.THAI_CONSONANTS:
                # This is final consonant, stop vowel collection
                break
            else:
                errors.append(ParseError(i, char, 'Unknown character in vowel area', text))
            
            i += 1
        
        # Remove processed characters
        text = text[i:]
        
        # Step 5: Extract final consonant (if any)
        final_consonant = None  # Changed from '' to None
        if text and text[0] in self.THAI_CONSONANTS:
            final_consonant = text[0]
            text = text[1:]
            
            # Check if final consonant is marked silent by ◌์ immediately after
            if text and text[0] == '์':
                final_consonant = None  # Silent final = no phonetic final
                text = text[1:]  # Remove silent marker
        
        # Check for leftover characters
        if text:
            errors.append(ParseError(len(text), text[0], 'Unexpected trailing characters', text))
        
        # Step 6: Reconstruct vowel form and determine length
        vowel_form = leading_vowel + vowel_above + vowel_below + vowel_trailing
        
        if not vowel_form:
            # Implicit vowel (rare, or reading single consonant as /Co/)
            vowel_form = 'implicit'
            vowel_length = 'short'
        else:
            # Look up vowel length
            vowel_length = self._determine_vowel_length(
                leading_vowel, vowel_above, vowel_below, vowel_trailing, final_consonant
            )
            
            if vowel_length is None:
                errors.append(ParseError(
                    0, vowel_form, 
                    f'Cannot determine vowel length for pattern: {vowel_form}',
                    leading_vowel + vowel_above + vowel_below + vowel_trailing
                ))
                vowel_length = 'unknown'
        
        # Step 7: Determine consonant class (with leading ห/อ modification)
        if consonant_cluster:
            # Cluster: class determined by first consonant
            consonant_class = self.consonant_classes.get(consonant_cluster[0], 'unknown')
        else:
            consonant_class = self.consonant_classes.get(initial_consonant, 'unknown')
        
        if consonant_class == 'unknown':
            errors.append(ParseError(
                0, initial_consonant,
                f'Unknown consonant class for {initial_consonant}',
                initial_consonant
            ))
        
        # Apply leading ห/อ modification
        effective_class = consonant_class
        if leading_h and consonant_class == 'low' and initial_consonant in self.SONORANTS:
            effective_class = 'high'
        elif leading_o and consonant_class == 'low':
            effective_class = 'mid'
        
        # Step 8: Determine if live or dead syllable
        is_live = self._is_live_syllable(vowel_length, final_consonant)
        
        # Step 9: Create SyllableAnalysis
        if consonant_class == 'unknown' or vowel_length == 'unknown':
            return None, errors
        
        analysis = SyllableAnalysis(
            initial_consonant=consonant_cluster if consonant_cluster else initial_consonant,
            consonant_class=consonant_class,
            vowel=vowel_form,
            vowel_length=vowel_length,
            final_consonant=final_consonant if final_consonant else None,
            tone_mark=tone_mark if tone_mark else None,
            is_live=is_live,
            effective_class=effective_class
        )
        
        return analysis, errors
    
    def _determine_vowel_length(
        self,
        leading: str,
        above: str,
        below: str,
        trailing: str,
        final: Optional[str]
    ) -> Optional[str]:
        """
        Determine vowel length from orthographic components.
        
        Returns 'short', 'long', or None if ambiguous.
        """
        # Common patterns
        if trailing == 'า':  # Long a
            return 'long'
        elif trailing == 'ะ':  # Short a
            return 'short'
        elif above in ['ิ', '็']:  # Short i or shortener
            return 'short'
        elif above == 'ี':  # Long i
            return 'long'
        elif above == 'ึ':  # Short ue
            return 'short'
        elif above == 'ื':  # Long ue
            return 'long'
        elif above == 'ั':  # Sara a shortener (typically short)
            return 'short'
        elif below == 'ุ':  # Short u
            return 'short'
        elif below == 'ู':  # Long u
            return 'long'
        elif leading == 'เ' and not trailing:
            # เ◌ can be short or long depending on final
            if final and final in self.STOPS:
                return 'short'
            else:
                return 'long'
        elif leading == 'แ':
            if trailing == 'ะ':
                return 'short'
            else:
                return 'long'
        elif leading == 'โ':  # Long o
            return 'long'
        elif leading in 'ใไ':  # ai diphthongs (long)
            return 'long'
        elif leading == 'เ' and trailing == 'า':  # ao (long)
            return 'long'
        elif 'ำ' in above or 'ำ' in trailing:  # am (short)
            return 'short'
        
        # If we can't determine, return None (ambiguous)
        return None
    
    def _is_live_syllable(self, vowel_length: str, final_consonant: Optional[str]) -> bool:
        """
        Determine if syllable is live or dead.
        
        Live: long vowel OR sonorant final
        Dead: short vowel + stop final OR short vowel + no final
        """
        if vowel_length == 'unknown':
            return True  # Default to live if unknown
        
        if final_consonant is None:
            # No final: live if long, dead if short
            return vowel_length == 'long'
        
        if final_consonant in self.SONORANTS:
            return True  # Always live with sonorant
        elif final_consonant in self.STOPS:
            # Stop final: live if long vowel, dead if short vowel
            return vowel_length == 'long'
        else:
            return True  # Unknown final, default to live

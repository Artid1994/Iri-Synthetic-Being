"""
Thai IPA Renderer
Converts SyllableAnalysis to IPA phonetic transcription
"""
import json
from pathlib import Path
from typing import Optional

from runtime.education.thai_tone_calculator import SyllableAnalysis


class ThaiIPARenderer:
    """
    Renders Thai syllables as IPA (International Phonetic Alphabet).
    
    Converts orthographic SyllableAnalysis to phonological IPA representation.
    """
    
    # Tone contours in Chao tone numbers (5-level scale)
    TONE_CONTOURS = {
        0: '˧',    # Mid tone (33)
        1: '˨˩',   # Low tone (21)
        2: '˥˩',   # Falling tone (51)
        3: '˦˥',   # High tone (45)
        4: '˨˩˦',  # Rising tone (214)
    }
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize with phonological data."""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "03_Hippocampus" / "knowledge_base" / "thai_language"
        
        self.data_dir = Path(data_dir)
        
        # Load consonant phonology
        consonant_phon_file = data_dir / "consonant_phonology.json"
        consonant_phon = json.loads(consonant_phon_file.read_text(encoding='utf-8'))
        
        self.consonant_ipa = {}
        self.consonant_final_ipa = {}
        for c in consonant_phon['consonant_phonemes']:
            # Strip slashes from IPA to get plain phoneme representation
            ipa_clean = c['ipa'].strip('/')
            self.consonant_ipa[c['grapheme']] = ipa_clean
            if c.get('final') and c['final'] != 'N/A':
                final_clean = c['final'].strip('/')
                self.consonant_final_ipa[c['grapheme']] = final_clean
        
        # Load vowel phonology
        vowel_phon_file = data_dir / "vowel_phonology.json"
        vowel_phon = json.loads(vowel_phon_file.read_text(encoding='utf-8'))
        
        # Map orthography to IPA (stripped of slashes)
        self.vowel_ipa = {}
        for v in vowel_phon['vowel_phonemes']:
            ipa_clean = v['ipa'].strip('/')
            for orth in v['orthography']:
                self.vowel_ipa[orth] = ipa_clean
    
    def render_ipa(self, analysis: SyllableAnalysis, tone: int, phonemic: bool = True) -> str:
        """
        Render complete IPA transcription with tone.
        
        Args:
            analysis: Parsed syllable structure
            tone: Tone number (0-4)
            phonemic: If True, wrap in /.../ (phonemic), else [...] (phonetic)
        
        Returns:
            IPA string with tone marking in standard notation
            
        Note:
            Internal phoneme representations have slashes stripped.
            Final output wraps complete transcription in / / or [ ].
        """
        phonemes = []
        
        # Initial consonant (or cluster)
        initial_ipa = self._get_initial_ipa(analysis.initial_consonant)
        if initial_ipa:
            phonemes.append(initial_ipa)
        
        # Vowel
        vowel_ipa = self._get_vowel_ipa(analysis.vowel)
        if vowel_ipa:
            phonemes.append(vowel_ipa)
        else:
            # Unknown vowel - mark explicitly
            phonemes.append('?')
        
        # Final consonant (if any)
        if analysis.final_consonant:
            final_ipa = self._get_final_ipa(analysis.final_consonant)
            if final_ipa:
                phonemes.append(final_ipa)
        
        # Tone contour
        tone_mark = self.TONE_CONTOURS.get(tone, '')
        if tone_mark:
            phonemes.append(tone_mark)
        
        # Join phonemes without internal separators
        transcription = ''.join(phonemes)
        
        # Wrap in standard IPA notation
        if phonemic:
            return f'/{transcription}/'
        else:
            return f'[{transcription}]'
    
    def _get_initial_ipa(self, initial: str) -> Optional[str]:
        """Get IPA for initial consonant or cluster (plain phonemes, no slashes)."""
        # Check if it's a cluster
        if len(initial) == 2:
            # Cluster: render both consonants
            c1_ipa = self.consonant_ipa.get(initial[0], f'{initial[0]}')
            c2_ipa = self.consonant_ipa.get(initial[1], f'{initial[1]}')
            return c1_ipa + c2_ipa
        else:
            return self.consonant_ipa.get(initial, f'{initial}')
    
    def _get_vowel_ipa(self, vowel: str) -> Optional[str]:
        """Get IPA for vowel (plain phoneme, no slashes)."""
        # Remove dotted circle placeholders if present
        vowel_clean = vowel.replace('◌', '')
        
        # Try direct lookup
        if vowel_clean in self.vowel_ipa:
            return self.vowel_ipa[vowel_clean]
        
        # Try each component separately for complex vowels
        if len(vowel_clean) > 1:
            for component in vowel_clean:
                if component in self.vowel_ipa:
                    return self.vowel_ipa[component]
        
        # Try with specific patterns (fallback for common vowels)
        if 'า' in vowel:
            return 'aː'
        elif 'ิ' in vowel:
            return 'i'
        elif 'ี' in vowel:
            return 'iː'
        elif 'ุ' in vowel:
            return 'u'
        elif 'ู' in vowel:
            return 'uː'
        elif 'เ' in vowel and not any(x in vowel for x in ['า', 'ะ']):
            return 'eː'
        elif 'แ' in vowel:
            return 'ɛː'
        elif 'โ' in vowel:
            return 'oː'
        elif 'ใ' in vowel or 'ไ' in vowel:
            return 'ai'
        
        # Unknown vowel
        return None
    
    def _get_final_ipa(self, final: str) -> Optional[str]:
        """Get IPA for final consonant (plain phoneme, no slashes)."""
        # Finals have different pronunciation than initials
        return self.consonant_final_ipa.get(final, self.consonant_ipa.get(final, f'{final}'))

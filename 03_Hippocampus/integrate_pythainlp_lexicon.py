#!/usr/bin/env python3
"""Integrate PyThaiNLP lexicon facts into Iri's Hippocampus."""

import json
from datetime import datetime

def integrate_lexicon_facts():
    """Load extracted facts and inject into knowledge base."""
    
    # Load extracted lexicon facts
    with open('/tmp/lexicon_facts.json', 'r', encoding='utf-8') as f:
        lexicon_facts = json.load(f)
    
    # Load Iri's knowledge base
    kb_path = 'knowledge_base.json'
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    original_count = len(kb['learned_facts'])
    
    # Add lexicon facts
    kb['learned_facts'].extend(lexicon_facts)
    kb['last_updated'] = datetime.now().isoformat()
    
    # Save updated knowledge base
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    new_count = len(kb['learned_facts'])
    
    print(f"✓ PyThaiNLP Lexicon integration complete")
    print(f"  Original facts: {original_count}")
    print(f"  Added lexicon facts: {len(lexicon_facts)}")
    print(f"  Total facts: {new_count}")
    print(f"  Updated: {kb['last_updated']}")
    
    return new_count

if __name__ == "__main__":
    integrate_lexicon_facts()

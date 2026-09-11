#!/usr/bin/env python3
"""
Hippocampus Fact Deduplication
Removes duplicate and near-duplicate facts while preserving high-confidence unique knowledge.
"""

import json
import hashlib
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict
from datetime import datetime


class FactDeduplicator:
    def __init__(self, knowledge_base_path: str):
        self.kb_path = Path(knowledge_base_path)
        self.backup_path = self.kb_path.parent / f"knowledge_base.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def load_knowledge_base(self) -> Dict:
        """Load knowledge base JSON."""
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_knowledge_base(self, kb: Dict, backup: bool = True):
        """Save deduplicated knowledge base with backup."""
        if backup and self.kb_path.exists():
            # Create backup
            with open(self.backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.load_knowledge_base(), f, indent=2, ensure_ascii=False)
            print(f"✓ Backup saved: {self.backup_path}")
        
        with open(self.kb_path, 'w', encoding='utf-8') as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        return ' '.join(text.lower().strip().split())
    
    def compute_hash(self, fact: Dict) -> str:
        """Compute hash of fact summary for exact duplicate detection."""
        summary = fact.get('summary', '')
        normalized = self.normalize_text(summary)
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute Jaccard similarity between two texts.
        Returns similarity score between 0.0 and 1.0.
        """
        words1 = set(self.normalize_text(text1).split())
        words2 = set(self.normalize_text(text2).split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def deduplicate_exact(self, facts: List[Dict]) -> List[Dict]:
        """Remove exact duplicates based on summary hash."""
        seen_hashes = {}
        unique_facts = []
        duplicates_removed = 0
        
        for fact in facts:
            fact_hash = self.compute_hash(fact)
            
            if fact_hash not in seen_hashes:
                seen_hashes[fact_hash] = fact
                unique_facts.append(fact)
            else:
                # Keep the one with higher confidence
                existing = seen_hashes[fact_hash]
                existing_conf = existing.get('confidence', 0.5)
                new_conf = fact.get('confidence', 0.5)
                
                if new_conf > existing_conf:
                    # Replace with higher confidence version
                    idx = unique_facts.index(existing)
                    unique_facts[idx] = fact
                    seen_hashes[fact_hash] = fact
                
                duplicates_removed += 1
        
        print(f"✓ Exact duplicates removed: {duplicates_removed}")
        return unique_facts
    
    def deduplicate_similar(self, facts: List[Dict], similarity_threshold: float = 0.85) -> List[Dict]:
        """
        Remove near-duplicates using similarity threshold.
        Keeps the fact with highest confidence among similar facts.
        """
        if not facts:
            return []
        
        # Sort by confidence descending so we keep high-confidence facts
        sorted_facts = sorted(facts, key=lambda f: f.get('confidence', 0.5), reverse=True)
        
        unique_facts = []
        removed_count = 0
        
        for candidate in sorted_facts:
            is_duplicate = False
            candidate_summary = candidate.get('summary', '')
            
            # Compare with already selected unique facts
            for unique_fact in unique_facts:
                unique_summary = unique_fact.get('summary', '')
                similarity = self.compute_similarity(candidate_summary, unique_summary)
                
                if similarity >= similarity_threshold:
                    is_duplicate = True
                    removed_count += 1
                    break
            
            if not is_duplicate:
                unique_facts.append(candidate)
        
        print(f"✓ Similar facts removed (threshold={similarity_threshold}): {removed_count}")
        return unique_facts
    
    def filter_low_confidence(self, facts: List[Dict], min_confidence: float = 0.3) -> List[Dict]:
        """Remove facts below minimum confidence threshold."""
        filtered = [f for f in facts if f.get('confidence', 0.5) >= min_confidence]
        removed = len(facts) - len(filtered)
        if removed > 0:
            print(f"✓ Low-confidence facts removed (< {min_confidence}): {removed}")
        return filtered
    
    def deduplicate(self, similarity_threshold: float = 0.85, min_confidence: float = 0.3) -> Dict:
        """
        Main deduplication pipeline:
        1. Remove exact duplicates
        2. Remove near-duplicates
        3. Filter low-confidence facts
        """
        print("🧠 Loading knowledge base...")
        kb = self.load_knowledge_base()
        
        facts = kb.get('learned_facts', [])
        original_count = len(facts)
        print(f"📊 Original fact count: {original_count}")
        
        if original_count == 0:
            print("⚠️  No facts to deduplicate")
            return kb
        
        print("\n🔍 Stage 1: Removing exact duplicates...")
        facts = self.deduplicate_exact(facts)
        
        print(f"\n🔍 Stage 2: Removing similar facts (threshold={similarity_threshold})...")
        facts = self.deduplicate_similar(facts, similarity_threshold)
        
        print(f"\n🔍 Stage 3: Filtering low-confidence facts (min={min_confidence})...")
        facts = self.filter_low_confidence(facts, min_confidence)
        
        final_count = len(facts)
        reduction = ((original_count - final_count) / original_count * 100) if original_count > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 DEDUPLICATION SUMMARY")
        print("=" * 60)
        print(f"Original facts:     {original_count}")
        print(f"Deduplicated facts: {final_count}")
        print(f"Facts removed:      {original_count - final_count}")
        print(f"Reduction:          {reduction:.1f}%")
        print("=" * 60)
        
        # Update knowledge base
        kb['learned_facts'] = facts
        kb['last_updated'] = datetime.now().isoformat()
        
        return kb


def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Deduplicate Hippocampus facts')
    parser.add_argument('--similarity', type=float, default=0.85,
                        help='Similarity threshold for near-duplicate detection (0.0-1.0)')
    parser.add_argument('--min-confidence', type=float, default=0.3,
                        help='Minimum confidence threshold (0.0-1.0)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview deduplication without saving')
    
    args = parser.parse_args()
    
    kb_path = Path(__file__).parent / "knowledge_base.json"
    
    if not kb_path.exists():
        print(f"✗ Knowledge base not found: {kb_path}")
        sys.exit(1)
    
    deduplicator = FactDeduplicator(str(kb_path))
    deduplicated_kb = deduplicator.deduplicate(
        similarity_threshold=args.similarity,
        min_confidence=args.min_confidence
    )
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No changes saved")
    else:
        print("\n💾 Saving deduplicated knowledge base...")
        deduplicator.save_knowledge_base(deduplicated_kb, backup=True)
        print("✅ Deduplication complete")


if __name__ == "__main__":
    main()

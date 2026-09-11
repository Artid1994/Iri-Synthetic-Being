#!/usr/bin/env python3
"""
Automatic Orphan Node Cross-Linking for Iri's Brain Atlas
Scans vault for orphan nodes and injects relevant backlinks.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class OrphanLinker:
    def __init__(self, vault_path: str = "/home/artid1994/Projects/THE_TRANSCENDING_FORM"):
        self.vault_path = Path(vault_path)
        self.wikilink_pattern = re.compile(r'\[\[([^\]]+)\]\]')
        
        # Brain region anchor nodes
        self.region_anchors = {
            "01_Neocortex": ["Logic", "Reasoning", "Planning", "Analysis"],
            "02_Limbic": ["Emotion", "Affective", "Motivation", "Reward"],
            "03_Hippocampus": ["Memory", "Learning", "Experience", "Recall"],
            "04_Cerebellum": ["Voice", "Speech", "Motor", "Coordination", "Daemon"]
        }
        
        # Concept keywords for semantic linking
        self.concept_keywords = {
            "Mathematics": ["math", "equation", "geometry", "algebra", "theorem", "proof"],
            "Science": ["biology", "physics", "chemistry", "scientific", "experiment"],
            "Language": ["english", "thai", "word", "grammar", "vocabulary", "สระ", "พยัญชนะ"],
            "Logic": ["reasoning", "deductive", "inductive", "logical", "argument"],
            "Philosophy": ["ethical", "philosophy", "knowledge", "epistemology"],
            "AI_Systems": ["ai", "model", "neural", "brain", "cognitive", "autonomous"]
        }
    
    def extract_wikilinks(self, content: str) -> Set[str]:
        """Extract all [[wikilinks]] from markdown content."""
        matches = self.wikilink_pattern.findall(content)
        return set(link.split('|')[0].strip() for link in matches)
    
    def scan_vault(self) -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
        """
        Scan all markdown files and build link graph.
        Returns: (outgoing_links_map, file_content_map)
        """
        outgoing_links = defaultdict(set)
        file_contents = {}
        
        # Exclude directories
        exclude_dirs = {'node_modules', '.obsidian', '.git', 'cognitive_shell_import', '__pycache__', '.venv', 'venv', '.pytest_cache'}
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip excluded directories
            if any(excl in md_file.parts for excl in exclude_dirs):
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    relative_path = str(md_file.relative_to(self.vault_path))
                    file_contents[relative_path] = content
                    links = self.extract_wikilinks(content)
                    if links:
                        outgoing_links[relative_path] = links
            except (UnicodeDecodeError, PermissionError):
                continue
        
        return outgoing_links, file_contents
    
    def find_orphans(self, outgoing_links: Dict[str, Set[str]], file_contents: Dict[str, str]) -> List[str]:
        """Identify files with 0 incoming or outgoing wikilinks."""
        all_files = set(file_contents.keys())
        files_with_outgoing = set(outgoing_links.keys())
        
        # Build incoming link map
        incoming_links = defaultdict(set)
        for source, targets in outgoing_links.items():
            for target in targets:
                # Match by basename (Obsidian wikilink behavior)
                for file_path in all_files:
                    if Path(file_path).stem == target or target in file_path:
                        incoming_links[file_path].add(source)
        
        # Find true orphans: no outgoing AND no incoming
        orphans = []
        for file_path in all_files:
            has_outgoing = file_path in files_with_outgoing
            has_incoming = file_path in incoming_links and len(incoming_links[file_path]) > 0
            
            if not has_outgoing and not has_incoming:
                orphans.append(file_path)
        
        return orphans
    
    def suggest_links(self, file_path: str, content: str) -> List[str]:
        """Suggest relevant wikilinks based on file path and content."""
        suggested = []
        content_lower = content.lower()
        
        # 1. Brain region anchor based on folder
        for region, keywords in self.region_anchors.items():
            if region.split('_')[1] in file_path or any(kw.lower() in file_path.lower() for kw in keywords):
                suggested.append(region)
                break
        
        # 2. Concept links based on content keywords
        for concept, keywords in self.concept_keywords.items():
            if any(kw in content_lower for kw in keywords):
                suggested.append(concept)
        
        # 3. Add parent brain region if in subfolders
        if "03_Hippocampus" in file_path or "03_Temporal" in file_path:
            if "03_Hippocampus" not in suggested:
                suggested.append("03_Hippocampus")
        elif "01_Neocortex" in file_path or "01_Frontal" in file_path:
            if "01_Neocortex" not in suggested:
                suggested.append("01_Neocortex")
        elif "02_Limbic" in file_path or "02_Parietal" in file_path:
            if "02_Limbic" not in suggested:
                suggested.append("02_Limbic")
        elif "04_Cerebellum" in file_path:
            if "04_Cerebellum" not in suggested:
                suggested.append("04_Cerebellum")
        
        return suggested[:5]  # Limit to 5 links to avoid clutter
    
    def inject_links(self, file_path: str, content: str, links: List[str]) -> str:
        """Inject wikilinks at the end of markdown file."""
        if not links:
            return content
        
        # Check if links section already exists
        if "## Related Concepts" in content or "## Neural Connections" in content:
            return content  # Already has links section
        
        links_section = "\n\n---\n\n## Neural Connections\n\n"
        links_section += " · ".join(f"[[{link}]]" for link in links)
        links_section += "\n"
        
        return content + links_section
    
    def process_orphans(self, dry_run: bool = False) -> Dict[str, any]:
        """Main processing: find orphans and inject links."""
        print("🔍 Scanning vault for orphan nodes...")
        outgoing_links, file_contents = self.scan_vault()
        
        print(f"📊 Found {len(file_contents)} markdown files")
        
        orphans = self.find_orphans(outgoing_links, file_contents)
        print(f"🔗 Identified {len(orphans)} orphan nodes")
        
        results = {
            "total_files": len(file_contents),
            "orphans_found": len(orphans),
            "orphans_linked": 0,
            "links_added": 0,
            "modified_files": []
        }
        
        for orphan_path in orphans:
            content = file_contents[orphan_path]
            suggested_links = self.suggest_links(orphan_path, content)
            
            if suggested_links:
                new_content = self.inject_links(orphan_path, content, suggested_links)
                
                if not dry_run:
                    full_path = self.vault_path / orphan_path
                    try:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        results["orphans_linked"] += 1
                        results["links_added"] += len(suggested_links)
                        results["modified_files"].append(orphan_path)
                        print(f"  ✓ Linked: {orphan_path} → {suggested_links}")
                    except Exception as e:
                        print(f"  ✗ Failed: {orphan_path} ({e})")
                else:
                    print(f"  [DRY RUN] Would link: {orphan_path} → {suggested_links}")
                    results["orphans_linked"] += 1
                    results["links_added"] += len(suggested_links)
        
        return results


def main():
    import sys
    
    dry_run = "--dry-run" in sys.argv
    
    linker = OrphanLinker()
    results = linker.process_orphans(dry_run=dry_run)
    
    print("\n" + "="*60)
    print("📊 ORPHAN LINKING RESULTS")
    print("="*60)
    print(f"Total markdown files: {results['total_files']}")
    print(f"Orphan nodes found: {results['orphans_found']}")
    print(f"Orphans linked: {results['orphans_linked']}")
    print(f"Total links added: {results['links_added']}")
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No files were modified")
        print("Run without --dry-run to apply changes")
    else:
        print(f"\n✅ Modified {len(results['modified_files'])} files")


if __name__ == "__main__":
    main()

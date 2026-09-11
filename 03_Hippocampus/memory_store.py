import os
from typing import Optional, List, Tuple
from pathlib import Path
from datetime import datetime

class HippocampusMemory:
    """
    Hippocampus Memory Node for Iri.
    Handles context retrieval, short-term conversational history, and knowledge search.
    """
    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = Path(vault_path or "/home/artid1994/Projects/THE_TRANSCENDING_FORM")
        self.short_term_history = []

    def _search_markdown_files(self, query: str, max_results: int = 3) -> List[Tuple[str, str]]:
        """
        Search for query in .md files within the vault.
        Returns list of (filename, relevant_snippet) tuples.
        """
        results = []
        query_lower = query.lower()
        
        try:
            for md_file in self.vault_path.rglob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        
                        # Search for query in content
                        for i, line in enumerate(lines):
                            if query_lower in line.lower():
                                # Get context: 2 lines before and after
                                start = max(0, i - 2)
                                end = min(len(lines), i + 3)
                                snippet = '\n'.join(lines[start:end])
                                results.append((md_file.name, snippet))
                                break
                        
                        if len(results) >= max_results:
                            break
                except (UnicodeDecodeError, PermissionError):
                    continue
        except Exception:
            pass
        
        return results

    def recall_context(self, query: str) -> str:
        """
        Retrieves relevant context for incoming query from Obsidian Vault.
        Scans .md files and returns relevant snippets.
        """
        if not query or not query.strip():
            return "ไม่มีข้อมูลค้นหาค่ะ"
        
        search_results = self._search_markdown_files(query)
        
        if not search_results:
            return f"ค้นหา '{query}' ในหน่วยความจำ แต่ไม่พบข้อมูลที่เกี่ยวข้องค่ะ"
        
        # Format context from search results
        context_parts = []
        for filename, snippet in search_results:
            context_parts.append(f"[{filename}]\n{snippet}")
        
        return "\n\n".join(context_parts)

    def add_history(self, role: str, message: str):
        self.short_term_history.append({"role": role, "message": message})
        if len(self.short_term_history) > 10:
            self.short_term_history.pop(0)
    
    def _extract_concept_links(self, topic: str, content: str) -> List[str]:
        """
        Extract relevant concept links based on topic and content keywords.
        Ensures every new insight is linked into the neural network.
        """
        links = set()
        content_lower = (topic + " " + content).lower()
        
        # Brain region anchors
        if any(kw in content_lower for kw in ["logic", "reasoning", "plan", "analyze", "think"]):
            links.add("01_Neocortex")
        if any(kw in content_lower for kw in ["emotion", "feel", "motivation", "reward", "affective"]):
            links.add("02_Limbic")
        if any(kw in content_lower for kw in ["memory", "learn", "experience", "recall", "remember"]):
            links.add("03_Hippocampus")
        if any(kw in content_lower for kw in ["voice", "speech", "motor", "coordinate", "daemon"]):
            links.add("04_Cerebellum")
        
        # Concept keywords
        concept_map = {
            "Mathematics": ["math", "equation", "geometry", "algebra", "theorem", "proof", "number"],
            "Science": ["biology", "physics", "chemistry", "scientific", "experiment", "cell"],
            "Language": ["english", "thai", "word", "grammar", "vocabulary", "สระ", "พยัญชนะ", "letter"],
            "Logic": ["reasoning", "deductive", "inductive", "logical", "argument", "premise"],
            "Philosophy": ["ethical", "philosophy", "knowledge", "epistemology", "ethics"],
            "AI_Systems": ["ai", "model", "neural", "brain", "cognitive", "autonomous", "agent"]
        }
        
        for concept, keywords in concept_map.items():
            if any(kw in content_lower for kw in keywords):
                links.add(concept)
        
        # Always link to parent Hippocampus region
        links.add("03_Hippocampus")
        
        return list(links)[:6]  # Limit to 6 links
    
    def consolidate_new_insight(self, topic: str, insight_content: str, category: str = "SEMANTIC") -> bool:
        """
        Autonomously write newly learned concepts as formatted markdown files.
        Automatically injects relevant concept backlinks to guarantee full Brain Atlas integration.
        """
        try:
            # Sanitize topic for filename
            safe_topic = topic.replace("/", "_").replace("\\", "_").replace(":", "_")
            safe_topic = safe_topic.replace(" ", "_")[:100]  # Limit length
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{category}_{safe_topic}_{timestamp}.md"
            
            # Target directory in Hippocampus
            insights_dir = self.vault_path / "03_Hippocampus" / "learned_insights"
            insights_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = insights_dir / filename
            
            # Extract relevant concept links for neural network integration
            concept_links = self._extract_concept_links(topic, insight_content)
            links_section = "\n\n---\n\n## Neural Connections\n\n"
            links_section += " · ".join(f"[[{link}]]" for link in concept_links)
            
            # Format markdown content with auto-injected backlinks
            markdown_content = f"""---
brain_region: hippocampus
category: {category.lower()}
topic: {topic}
learned_at: {datetime.now().isoformat()}
source: autonomous_consolidation
---

# {topic}

{insight_content}

{links_section}

---

**Consolidated by:** Iri (AE01M) Autonomous Learning System  
**Timestamp:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return True
        except Exception:
            return False

if __name__ == "__main__":
    memory = HippocampusMemory()
    res = memory.recall_context("ระบบความจำ")
    print(f"💾 [Hippocampus Recall]: {res}")

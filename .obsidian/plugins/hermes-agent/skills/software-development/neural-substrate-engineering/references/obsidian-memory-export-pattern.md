# MemoryGraph to Obsidian Export Contract Pattern

## Objective
Export an in-memory knowledge or memory graph (e.g. `MemoryGraph`) into an Obsidian-compatible directory of Markdown notes with Wikilinks, preserving graph ownership in the core runtime while preventing corruption, collision, or accidental deletion of user files.

## Architectural Boundaries
1. **Single Source of Truth**: The core runtime memory graph owns all nodes and edges. The exported files are strictly a one-way, read-only external projection.
2. **Directory Isolation**: Exports must target a designated, isolated directory (e.g., `test_vault_export/` or `vault/memory_projection/`). Never overwrite or delete files outside this directory.
3. **No Private Mutation**: Read only public graph attributes (`graph.nodes`, `graph.edges`).

## Exporter Implementation Pattern
```python
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

MANIFEST_FILENAME = ".ae01m_memory_manifest.json"

def sanitize_filename(content: str, max_length: int = 60) -> str:
    cleaned = re.sub(r"[^\w\-]+", "_", content.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return (cleaned or "item")[:max_length]

class ObsidianMemoryExporter:
    def __init__(self, export_dir: Path | str) -> None:
        self.export_dir = Path(export_dir).resolve()

    def _get_filename_mapping(self, graph) -> dict[str, str]:
        mapping = {}
        used_stems = {}
        for node_id in sorted(graph.nodes.keys()):
            node = graph.nodes[node_id]
            clean_content = sanitize_filename(node.content)
            clean_type = sanitize_filename(node.memory_type)
            base_stem = f"{clean_type}__{clean_content}"
            if base_stem not in used_stems:
                used_stems[base_stem] = node_id
                mapping[node_id] = base_stem
            else:
                short_hash = hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:8]
                collision_stem = f"{base_stem}_{short_hash}"
                used_stems[collision_stem] = node_id
                mapping[node_id] = collision_stem
        return mapping
```

## Wikilink Resolution
Obsidian parses native Wikilinks in the form:
`[[target_stem|Target Label]]` (without the `.md` extension).
Outgoing edges must map to the sanitized target stem so that Obsidian's graph indexer resolves the edge correctly.

## Manifest and Pruned Node Cleanup
To support memory pruning/decay without deleting user-created notes:
- Maintain an exporter-owned JSON manifest `.ae01m_memory_manifest.json` mapping `node_id -> relative_filename`.
- When exporting, compare previous manifest entries to current nodes.
- Only delete files that (1) are recorded in the manifest, (2) are inside `export_dir`, (3) end with `.md`, and (4) no longer exist in the graph.

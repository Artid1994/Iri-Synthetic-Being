from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.memory_graph import MemoryGraph


MANIFEST_FILENAME = ".ae01m_memory_manifest.json"


def sanitize_filename(content: str, max_length: int = 60) -> str:
    """Sanitize content string to create a safe, deterministic filename base."""
    # Replace non-alphanumeric characters (except dashes and underscores) with underscores
    cleaned = re.sub(r"[^\w\-]+", "_", content.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        cleaned = "item"
    return cleaned[:max_length]


class ObsidianMemoryExporter:
    """One-way, read-only projection exporter from AE01M MemoryGraph to Obsidian-compatible Markdown."""

    def __init__(self, export_dir: Path | str) -> None:
        self.export_dir = Path(export_dir).resolve()

    def _get_filename_mapping(self, graph: MemoryGraph) -> dict[str, str]:
        """Produce deterministic, collision-free filename stems for all nodes in the graph."""
        mapping: dict[str, str] = {}
        used_stems: dict[str, str] = {}  # stem -> node_id

        # Sort node keys to ensure deterministic ordering across runs
        sorted_node_ids = sorted(graph.nodes.keys())

        for node_id in sorted_node_ids:
            node = graph.nodes[node_id]
            clean_content = sanitize_filename(node.content)
            clean_type = sanitize_filename(node.memory_type)
            base_stem = f"{clean_type}__{clean_content}"

            if base_stem not in used_stems:
                used_stems[base_stem] = node_id
                mapping[node_id] = base_stem
            else:
                # Collision detected: append short deterministic hash of node_id
                short_hash = hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:8]
                collision_stem = f"{base_stem}_{short_hash}"
                used_stems[collision_stem] = node_id
                mapping[node_id] = collision_stem

        return mapping

    def _load_manifest(self) -> dict[str, str]:
        manifest_path = self.export_dir / MANIFEST_FILENAME
        if not manifest_path.is_file():
            return {}
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return {str(k): str(v) for k, v in data.get("managed_files", {}).items()}
        except Exception:
            return {}
        return {}

    def _save_manifest(self, managed_files: dict[str, str]) -> None:
        manifest_path = self.export_dir / MANIFEST_FILENAME
        payload = {
            "version": 1,
            "generator": "AE01M ObsidianMemoryExporter",
            "managed_files": managed_files,  # node_id -> rel_filename
        }
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def export(self, graph: MemoryGraph) -> dict[str, int]:
        """Export the given MemoryGraph to the designated isolated directory.

        Returns statistics: {'exported': count, 'cleaned': count}.
        """
        # Ensure export directory exists safely
        self.export_dir.mkdir(parents=True, exist_ok=True)

        prev_manifest = self._load_manifest()
        name_mapping = self._get_filename_mapping(graph)

        current_managed: dict[str, str] = {}
        exported_count = 0

        # Export active nodes
        for node_id, stem in name_mapping.items():
            node = graph.nodes[node_id]
            rel_filename = f"{stem}.md"
            file_path = self.export_dir / rel_filename

            # Identify outgoing edges from this node
            out_edges = [
                edge
                for edge in graph.edges.values()
                if edge.source == node_id
            ]
            out_edges.sort(key=lambda e: (e.target, e.weight), reverse=True)

            associations_lines = []
            for edge in out_edges:
                target_stem = name_mapping.get(edge.target)
                target_node = graph.nodes.get(edge.target)
                target_label = target_node.content if target_node else edge.target
                if target_stem:
                    associations_lines.append(
                        f"- [[{target_stem}|{target_label}]] (weight: {edge.weight:.2f}, usage: {edge.usage_count})"
                    )
                else:
                    associations_lines.append(
                        f"- `{edge.target}` (weight: {edge.weight:.2f}, usage: {edge.usage_count})"
                    )

            associations_block = "\n".join(associations_lines) if associations_lines else "No outgoing associations."

            # Construct Markdown content with YAML frontmatter
            escaped_content = node.content.replace('"', '\\"')
            escaped_type = node.memory_type.replace('"', '\\"')
            escaped_id = node_id.replace('"', '\\"')

            md_content = (
                f"---\n"
                f'id: "{escaped_id}"\n'
                f'type: "{escaped_type}"\n'
                f"activation_count: {node.activation_count}\n"
                f"---\n\n"
                f"# {node.content}\n\n"
                f"## Associations\n"
                f"{associations_block}\n\n"
                f"## Projection Info\n"
                f"- **Memory Type**: {node.memory_type}\n"
                f"- **Activation Count**: {node.activation_count}\n"
            )

            # Write file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            current_managed[node_id] = rel_filename
            exported_count += 1

        # Clean up files for nodes that were previously managed but are no longer in graph
        cleaned_count = 0
        for old_node_id, old_rel_file in prev_manifest.items():
            if old_node_id not in current_managed:
                old_file_path = self.export_dir / old_rel_file
                # Safety checks: must be within export_dir, must be .md, must exist
                try:
                    resolved_old = old_file_path.resolve()
                    if self.export_dir in resolved_old.parents and resolved_old.suffix == ".md" and resolved_old.is_file():
                        resolved_old.unlink()
                        cleaned_count += 1
                except Exception:
                    pass

        # Save updated manifest
        self._save_manifest(current_managed)

        return {"exported": exported_count, "cleaned": cleaned_count}

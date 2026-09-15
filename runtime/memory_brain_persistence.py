from __future__ import annotations

import os
import json
from pathlib import Path
from typing import TYPE_CHECKING

from runtime.memory import Memory, MemoryState
from runtime.experience import Experience
from runtime.safety_event import SafetyEvent
from runtime.memory_graph import MemoryGraph, MemoryNode, MemoryEdge

# Brain module archived - make optional
if TYPE_CHECKING:
    from brain.brain import Brain
else:
    try:
        from brain.brain import Brain
    except ImportError:
        Brain = None

class PersistenceSchemaError(ValueError):
    """Raised when persisted data violates schema or version contracts."""
    pass

class MemoryBrainPersistence:
    """
    Deterministic, versioned persistence manager for Memory and Brain subsystems.
    Strictly preserves subsystem boundaries:
    - Memory subsystem owns working, episodic, semantic, experiences, safety events, and MemoryGraph.
    - Brain subsystem owns hippocampus memories.
    """
    VERSION = "1.0.0"

    @classmethod
    def serialize_memory(cls, memory: Memory) -> dict:
        if not isinstance(memory, Memory):
            raise TypeError("memory must be a Memory instance")

        state = memory.state
        graph = memory.memory_graph

        nodes_data = {
            node_id: {
                "content": node.content,
                "memory_type": node.memory_type,
                "activation_count": node.activation_count,
                "source_url": node.source_url,
                "retrieval_timestamp": node.retrieval_timestamp,
                "confidence": node.confidence,
            }
            for node_id, node in graph.nodes.items()
        }

        edges_data = [
            {
                "source": edge.source,
                "target": edge.target,
                "weight": edge.weight,
                "usage_count": edge.usage_count,
            }
            for edge in graph.edges.values()
        ]

        experiences_data = [
            {
                "source": exp.source,
                "content": exp.content,
                "timestamp": exp.timestamp,
                "modality": exp.modality,
                "salience": exp.salience,
            }
            for exp in state.experiences
        ]

        safety_events_data = [
            {
                "action": event.action,
                "value": event.value if not isinstance(event.value, (tuple, list)) else list(event.value),
                "reason": event.reason,
            }
            for event in state.safety_events
        ]

        associations_data = memory._association_index.snapshot()

        return {
            "version": cls.VERSION,
            "subsystem": "memory",
            "state": {
                "working": list(state.working),
                "episodic": list(state.episodic),
                "semantic": list(state.semantic),
                "experiences": experiences_data,
                "safety_events": safety_events_data,
                "associations": associations_data,
            },
            "graph": {
                "nodes": nodes_data,
                "edges": edges_data,
            },
        }

    @classmethod
    def deserialize_memory(cls, data: dict, memory: Memory | None = None) -> Memory:
        if not isinstance(data, dict):
            raise TypeError("Persistence data must be a dictionary")

        if data.get("version") != cls.VERSION:
            raise PersistenceSchemaError(f"Incompatible persistence version: {data.get('version')}")

        if data.get("subsystem") != "memory":
            raise PersistenceSchemaError(f"Invalid subsystem tag: {data.get('subsystem')}")

        state_data = data.get("state")
        graph_data = data.get("graph")
        if not isinstance(state_data, dict) or not isinstance(graph_data, dict):
            raise PersistenceSchemaError("Corrupted memory payload: missing state or graph section")

        target_memory = memory if memory is not None else Memory()

        # Restore working, episodic, semantic
        target_memory.state.working = list(state_data.get("working", []))
        target_memory.state.episodic = list(state_data.get("episodic", []))
        target_memory.state.semantic = list(state_data.get("semantic", []))

        # Rebuild indexes
        target_memory._recall_index.rebuild(target_memory.state.episodic)
        for s in target_memory.state.semantic:
            target_memory._semantic_index.add(s)

        # Restore experiences
        target_memory.state.experiences = [
            Experience(
                source=exp["source"],
                content=exp["content"],
                timestamp=exp["timestamp"],
                modality=exp["modality"],
                salience=exp["salience"],
            )
            for exp in state_data.get("experiences", [])
        ]

        # Restore safety events
        target_memory.state.safety_events = [
            SafetyEvent(
                action=sev["action"],
                value=tuple(sev["value"]) if isinstance(sev["value"], list) else sev["value"],
                reason=sev["reason"],
            )
            for sev in state_data.get("safety_events", [])
        ]

        # Restore associations
        for exp, assocs in state_data.get("associations", {}).items():
            for a in assocs:
                target_memory._association_index.add(exp, a)

        # Restore MemoryGraph
        target_memory.memory_graph.nodes.clear()
        target_memory.memory_graph.edges.clear()
        target_memory.memory_graph.active_nodes.clear()
        target_memory.memory_graph.active_edges.clear()

        for node_id, n_dict in graph_data.get("nodes", {}).items():
            node = MemoryNode(
                content=n_dict["content"],
                memory_type=n_dict["memory_type"],
                activation_count=n_dict.get("activation_count", 1),
                source_url=n_dict.get("source_url"),
                retrieval_timestamp=n_dict.get("retrieval_timestamp"),
                confidence=n_dict.get("confidence"),
            )
            target_memory.memory_graph.nodes[node_id] = node

        for e_dict in graph_data.get("edges", []):
            edge = MemoryEdge(
                source=e_dict["source"],
                target=e_dict["target"],
                weight=e_dict.get("weight", 1.0),
                usage_count=e_dict.get("usage_count", 1),
            )
            target_memory.memory_graph.edges[(edge.source, edge.target)] = edge

        return target_memory

    @classmethod
    def serialize_brain(cls, brain: Brain) -> dict:
        if not isinstance(brain, Brain):
            raise TypeError("brain must be a Brain instance")

        # Hippocampus owned memories
        memories = sorted(brain.hippocampus._memories)

        return {
            "version": cls.VERSION,
            "subsystem": "brain",
            "hippocampus": {
                "memories": memories,
            },
        }

    @classmethod
    def deserialize_brain(cls, data: dict, brain: Brain | None = None) -> Brain:
        if not isinstance(data, dict):
            raise TypeError("Persistence data must be a dictionary")

        if data.get("version") != cls.VERSION:
            raise PersistenceSchemaError(f"Incompatible persistence version: {data.get('version')}")

        if data.get("subsystem") != "brain":
            raise PersistenceSchemaError(f"Invalid subsystem tag: {data.get('subsystem')}")

        hippo_data = data.get("hippocampus")
        if not isinstance(hippo_data, dict) or "memories" not in hippo_data:
            raise PersistenceSchemaError("Corrupted brain payload: missing hippocampus section")

        target_brain = brain if brain is not None else Brain()
        for mem in hippo_data["memories"]:
            target_brain.store_memory(mem)

        return target_brain

    @classmethod
    def save(cls, memory: Memory, brain: Brain, filepath: Path | str) -> None:
        payload = {
            "version": cls.VERSION,
            "type": "ae01m_memory_brain_snapshot",
            "memory": cls.serialize_memory(memory),
            "brain": cls.serialize_brain(brain),
        }
        target_path = Path(filepath).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        tmp_path = target_path.with_suffix(".tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, target_path)
        except Exception:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            raise

    @classmethod
    def load(cls, filepath: Path | str, memory: Memory | None = None, brain: Brain | None = None) -> tuple[Memory, Brain]:
        target_path = Path(filepath).resolve()
        if not target_path.exists():
            raise FileNotFoundError(f"Persistence file not found: {target_path}")

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except Exception as exc:
            raise PersistenceSchemaError(f"Failed to read persistence file: {exc}") from exc

        if not isinstance(payload, dict):
            raise PersistenceSchemaError("Payload must be a JSON object")

        if payload.get("version") != cls.VERSION:
            raise PersistenceSchemaError(f"Incompatible file version: {payload.get('version')}")

        if payload.get("type") != "ae01m_memory_brain_snapshot":
            raise PersistenceSchemaError(f"Invalid snapshot type: {payload.get('type')}")

        mem_dict = payload.get("memory")
        brain_dict = payload.get("brain")
        if not isinstance(mem_dict, dict) or not isinstance(brain_dict, dict):
            raise PersistenceSchemaError("Corrupted snapshot: missing memory or brain data")

        restored_memory = cls.deserialize_memory(mem_dict, memory=memory)
        restored_brain = cls.deserialize_brain(brain_dict, brain=brain)

        return restored_memory, restored_brain

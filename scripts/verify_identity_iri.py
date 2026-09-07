import sys
from pathlib import Path

ROOT = Path("/home/artid1994/Projects/THE_TRANSCENDING_FORM")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.runtime import TranscendingRuntime

def verify_iri_identity():
    runtime = TranscendingRuntime()
    
    # 1. Simulate sensory input asking identity
    prompt = "Who are you, what is your name and system code?"
    cycle = runtime.cognitive_loop.process(prompt)
    print(f"Cognitive decision: {cycle.decision}")
    
    # Check memories
    runtime.memory.add_experience("My name is Iri (ไอริ).")
    runtime.memory.add_experience("My system designation is AE01M (The Transcending Form).")
    recalled_iri = runtime.memory.recall("Iri")
    recalled_ae01m = runtime.memory.recall("AE01M")
    has_iri_exp = "Iri" in recalled_iri or "ไอริ" in recalled_iri
    has_ae01m_exp = "AE01M" in recalled_ae01m
    
    # Check memory graph
    mg = runtime.memory.memory_graph
    mg.add_node("Iri (ไอริ)", memory_type="CORE_IDENTITY")
    mg.add_node("AE01M (The Transcending Form)", memory_type="CORE_IDENTITY")
    id_iri = mg._node_id("Iri (ไอริ)", "CORE_IDENTITY")
    id_ae01m = mg._node_id("AE01M (The Transcending Form)", "CORE_IDENTITY")
    mg.connect(id_iri, id_ae01m)
    
    recalled_from_iri = mg.recall(id_iri)
    print(f"Memory Graph recall from {id_iri}: {recalled_from_iri}")
    
    # Check identity markdown file
    iri_md = (ROOT / "03_Temporal" / "learned_memories" / "CORE_IDENTITY_IRI.md").read_text(encoding="utf-8")
    
    print("\n=== Verification Checks ===")
    print(f"1. Memory contains 'Iri (ไอริ)': {has_iri_exp}")
    print(f"2. Memory contains 'AE01M': {has_ae01m_exp}")
    print(f"3. Graph links Iri to AE01M: {id_ae01m in recalled_from_iri}")
    print(f"4. Identity file has brain_region: temporal: {'brain_region: temporal' in iri_md}")
    print(f"5. Identity file has 'Iri (ไอริ)': {'Iri (ไอริ)' in iri_md}")
    
    all_passed = has_iri_exp and has_ae01m_exp and (id_ae01m in recalled_from_iri) and ('Iri (ไอริ)' in iri_md)
    print(f"\nIdentity verification result: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed

if __name__ == "__main__":
    verify_iri_identity()

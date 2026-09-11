#!/usr/bin/env python3
import importlib.util
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Dynamic import handling for numerical folder names
def import_from_numerical_path(module_path, class_name):
    """Import a class from a module in a numerically-prefixed folder."""
    spec = importlib.util.spec_from_file_location(f"dynamic_{class_name}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return getattr(module, class_name)

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent

# Import all 4 brain layer components
ExecutiveCore = import_from_numerical_path(
    PROJECT_ROOT / "01_Neocortex" / "executive_core.py",
    "ExecutiveCore"
)

LimbicAffect = import_from_numerical_path(
    PROJECT_ROOT / "02_Limbic" / "affective_filter.py",
    "LimbicAffect"
)

HippocampusMemory = import_from_numerical_path(
    PROJECT_ROOT / "03_Hippocampus" / "memory_store.py",
    "HippocampusMemory"
)

# Import speak function
voice_synthesis_spec = importlib.util.spec_from_file_location(
    "voice_synthesis",
    PROJECT_ROOT / "04_Cerebellum" / "voice_synthesis.py"
)
if voice_synthesis_spec is None or voice_synthesis_spec.loader is None:
    raise ImportError("Cannot load voice_synthesis module")
voice_synthesis = importlib.util.module_from_spec(voice_synthesis_spec)
sys.modules[voice_synthesis_spec.name] = voice_synthesis
voice_synthesis_spec.loader.exec_module(voice_synthesis)
speak_sync = voice_synthesis.speak


class IriVoiceLoop:
    """
    Integrated Voice Interactive Loop for Iri (AE01M).
    Coordinates all 4 brain layers: Neocortex → Limbic → Hippocampus → Cerebellum
    """
    
    def __init__(self):
        # Initialize all 4 brain layer nodes
        self.hippocampus = HippocampusMemory()
        self.neocortex = ExecutiveCore()
        self.limbic = LimbicAffect()
    
    async def speak(self, text: str, emotional_state=None):
        """Async wrapper for voice synthesis with emotional state."""
        loop = asyncio.get_event_loop()
        if emotional_state is not None:
            await loop.run_in_executor(None, lambda: speak_sync(text, emotional_state))
        else:
            await loop.run_in_executor(None, speak_sync, text)
    
    async def process_and_respond(self, user_input: str):
        """
        Complete cognitive pipeline integrating all 4 brain layers with autonomous learning.
        
        Step 1: Recall context from Hippocampus (memory)
        Step 2: Process thought through Neocortex (reasoning)
        Step 3: Evaluate tone through Limbic (affective filter)
        Step 4: Synthesize speech through Cerebellum (motor output)
        Step 5: Update weights and persist learned state
        """
        # Step 1: Memory context retrieval
        memory_context = self.hippocampus.recall_context(user_input)
        
        # Step 2: Executive reasoning with memory context
        raw_thought = self.neocortex.process_thought(user_input, memory_context=memory_context)
        
        # Step 3: Affective tone evaluation
        final_response = self.limbic.evaluate_tone(raw_thought)
        
        # Step 4: Voice synthesis output with emotional state
        current_emotional_state = self.limbic.get_current_state()
        await self.speak(final_response, emotional_state=current_emotional_state)
        
        # Store interaction in short-term history
        self.hippocampus.add_history("user", user_input)
        self.hippocampus.add_history("assistant", final_response)
        
        # Step 5: Autonomous learning - persist state after interaction
        # Save Neocortex learned weights
        self.neocortex.save_neocortex_state()
        
        # If new high-value concepts emerged, consolidate to Hippocampus
        if hasattr(self.neocortex, 'active_context') and 'last_concepts' in self.neocortex.active_context:
            concepts = self.neocortex.active_context['last_concepts']
            for concept in concepts[:1]:  # Consolidate top concept if highly relevant
                if concept.relevance > 0.8 and concept.related_facts:
                    insight = f"เรียนรู้จากการสนทนา: {user_input}\n\n"
                    insight += "\n".join(concept.related_facts[:3])
                    self.hippocampus.consolidate_new_insight(
                        topic=concept.name,
                        insight_content=insight,
                        category="EPISODIC"
                    )
        
        return final_response


async def main():
    """Interactive mode - listens to Named Pipe (FIFO) for daemon communication."""
    iri = IriVoiceLoop()
    
    # Named pipe path for daemon communication
    fifo_path = Path("/tmp/iri_input.fifo")
    
    # Create FIFO if it doesn't exist
    if not fifo_path.exists():
        os.mkfifo(fifo_path)
        print(f"✓ Created named pipe: {fifo_path}")
    
    print("=" * 60)
    print("Iri (AE01M) - Autonomous Voice Loop Daemon")
    print("=" * 60)
    print(f"Listening on: {fifo_path}")
    print("Send messages using: iri \"your message here\"")
    print()
    
    try:
        while True:
            try:
                # Open FIFO in non-blocking mode for reading
                # This will block until someone writes to the pipe
                loop = asyncio.get_event_loop()
                
                # Read from FIFO asynchronously
                def read_fifo():
                    with open(fifo_path, 'r') as fifo:
                        return fifo.readline().strip()
                
                user_input = await loop.run_in_executor(None, read_fifo)
                
                if not user_input:
                    continue  # Empty line, wait for next message
                
                # Exit commands
                if user_input.lower() in ['exit', 'quit', 'shutdown', 'ออก']:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🤖 Iri: ลาก่อนค่ะ เจ้านาย (Shutdown requested)")
                    break
                
                # Process and respond
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] 👤 User: {user_input}")
                print(f"[{timestamp}] 🤖 Iri: ", end="", flush=True)
                
                response = await iri.process_and_respond(user_input)
                print(response)
                print()
                
            except Exception as e:
                print(f"[ERROR] {e}")
                await asyncio.sleep(1)
                
    except KeyboardInterrupt:
        print("\n🤖 Iri: ลาก่อนค่ะ (Daemon stopped)")
    finally:
        # Clean up FIFO on exit
        if fifo_path.exists():
            fifo_path.unlink()
            print(f"✓ Cleaned up: {fifo_path}")


if __name__ == "__main__":
    asyncio.run(main())

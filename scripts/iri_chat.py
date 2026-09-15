#!/usr/bin/env python3
"""
Iri Interactive Chat Terminal
Real-time conversational interface with AE01M cognitive system.
"""
import sys
import os
import json
import time
import threading
import importlib
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add project root to path FIRST (before any local imports)
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))
sys.path.insert(0, str(PROJECT_ROOT / "03_Hippocampus"))
sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))

# Import Neocortex and Hippocampus
try:
    from executive_core import KnowledgeGraph, Intent
    from memory_store import HippocampusMemory
    from core_directives import CoreDirectives
    from nlp_thai_lexicon import get_thai_lexicon
    from skills import get_system_inspector, get_text_analyzer

    # Communication modules (with proper path)
    sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex" / "tools"))
    from bilingual_pragmatics import BilingualPragmaticParser
    from conversational_response_builder import ConversationalResponseBuilder, ResponseContext

    # Cognitive modules
    from inner_monologue import InnerMonologue
    from parallel_processor import get_processor
    
    # Semantic learning modules
    from semantic_extractor import SemanticExtractor
    from semantic_knowledge import SemanticKnowledgeStore
    
    # Voice serialization
    sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))
    from voice_serializer import get_voice_serializer

except ImportError as e:
    print(f"⚠️  Import error: {e}")
    print("Make sure you're running from project root with venv activated")
    sys.exit(1)

class IriChat:
    """Interactive chat session with Iri."""

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.knowledge = KnowledgeGraph()
        self.memory = HippocampusMemory(vault_path=str(PROJECT_ROOT))
        self.directives = CoreDirectives
        self.thai_lexicon = get_thai_lexicon()
        self.system_inspector = get_system_inspector()
        self.text_analyzer = get_text_analyzer()
        self.conversation_history = []

        # State file for user activity detection (DIRECTIVE_2)
        self.state_file = PROJECT_ROOT / "04_Cerebellum" / "iri_state.json"
        self.update_user_activity()

        # Session metadata
        self.session_start = datetime.now()
        self.session_id = int(self.session_start.timestamp())

        # Voice synthesis (direct integration with VoiceSynthesizer)
        self.voice_synthesizer = None
        self._init_voice_synthesis()

        # Bilingual pragmatic parser
        self.bilingual_parser = BilingualPragmaticParser()
        print("✓ Bilingual parser initialized")

        # Conversational response builder
        self.response_builder = ConversationalResponseBuilder()
        print("✓ Natural response generator initialized")

        # Inner monologue pipeline
        self.inner_monologue = InnerMonologue(PROJECT_ROOT)
        print("✓ Inner monologue reasoning initialized")

        # Parallel processor
        self.parallel_processor = get_processor()
        print("✓ Parallel dual-tasking engine started")
        
        # Semantic learning components
        self.semantic_extractor = SemanticExtractor()
        self.semantic_knowledge = SemanticKnowledgeStore(
            storage_path=PROJECT_ROOT / "03_Hippocampus" / "semantic_facts.json"
        )
        print("✓ Semantic learning system initialized")
        
        # Voice serializer for non-overlapping playback
        self.voice_serializer = get_voice_serializer()
        print("✓ Voice serialization enabled")

    def _init_voice_synthesis(self):
        """Initialize VoiceSynthesizer dynamically from 04_Cerebellum."""
        try:
            voice_synthesis_module = importlib.import_module('voice_synthesis')
            VoiceSynthesizer = voice_synthesis_module.VoiceSynthesizer
            self.voice_synthesizer = VoiceSynthesizer(
                voice_th="th-TH-NiwatNeural",
                voice_en="en-US-JennyNeural",
                rate="+5%",
                volume="+0%",
                player_cmd="ffplay",
                enabled=True
            )
            print(f"✓ Voice synthesis: enabled (Thai male: th-TH-NiwatNeural)")
        except Exception as e:
            print(f"⚠️  Voice synthesis unavailable: {e}")
            self.voice_synthesizer = None

    def update_user_activity(self):
        """Update user activity timestamp (DIRECTIVE_2 compliance)."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            state = {}
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)

            state['last_activity'] = time.time()
            state['mode'] = 'interactive'

            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass

    def speak(self, text: str):
        """
        Speak text using TTS voice synthesis with serialized playback.
        Uses VoiceSynthesizer with proper PipeWire environment and voice serializer
        to prevent overlapping audio.
        """
        if not self.voice_synthesizer or not text or not text.strip():
            return

        try:
            # Enforce PipeWire/PulseAudio environment
            env = os.environ.copy()
            env['XDG_RUNTIME_DIR'] = '/run/user/1000'
            env['PULSE_SERVER'] = 'unix:/run/user/1000/pulse/native'

            # Synthesize audio file
            audio_file = self.voice_synthesizer.synthesize(text)
            
            if audio_file and os.path.exists(audio_file):
                # Cleanup callback to remove temp file after playback
                def cleanup(file_path):
                    if "/tmp" in file_path:
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass
                
                # Queue for serialized playback (cancels any currently playing audio)
                self.voice_serializer.play(audio_file, env, cleanup)
                
        except Exception as e:
            # Silent failure - don't interrupt conversation flow
            pass

    def classify_input(self, user_input: str) -> Intent:
        """Classify user input intent using Thai NLP lexicon and skills."""
        user_lower = user_input.lower()

        # Use Thai lexicon for advanced entity extraction
        thai_intent = self.thai_lexicon.extract_intent(user_input)

        # Check for system inspection keywords (highest priority)
        system_keywords = [
            'ตรวจสอบ', 'สถานะ', 'ระบบ', 'รายงาน', 'วิเคราะห์',
            'ตรวจสภาพ', 'เครื่อง', 'ตรวจ', 'สภาพ', 'เป็นไง',
            'เป็นยังไง', 'ตรวจดู', 'รายงานผล'
        ]
        if any(keyword in user_input for keyword in system_keywords):
            # Use text analyzer to extract precise skill command
            skill_command = self.text_analyzer.extract_skill_commands(user_input)
            if skill_command:
                return Intent(
                    type='skill',
                    confidence=1.0,
                    entities=[skill_command['skill'], skill_command['method']]
                )
            # Fallback to full system inspection
            return Intent(
                type='skill',
                confidence=0.9,
                entities=['system_inspector', 'inspect_all']
            )

        # Check for other skill commands
        skill_command = self.text_analyzer.extract_skill_commands(user_input)
        if skill_command:
            return Intent(
                type='skill',
                confidence=1.0,
                entities=[skill_command['skill'], skill_command['method']]
            )

        # Exit detection - match whole words only to avoid false positives
        # (e.g., "ออกหาอาหาร" contains "ออก" but is not an exit command)
        import re
        exit_patterns = [
            r'\bexit\b', r'\bquit\b', r'\bbye\b',  # English
            r'\bออก\b', r'\bลาก่อน\b'  # Thai (with word boundaries)
        ]
        if any(re.search(pattern, user_lower) for pattern in exit_patterns):
            return Intent(type='exit', confidence=1.0, entities=['exit'])

        # Question detection (check before greeting to prioritize questions)
        if any(q in user_lower for q in ['?', 'what', 'why', 'how', 'when', 'who',
                                          'อะไร', 'ทำไม', 'อย่างไร', 'เมื่อไหร่']):
            return Intent(type='question', confidence=0.8, entities=thai_intent.get('entities', {}).get('object', []))

        # Greeting detection - only if short and primarily a greeting
        # Don't classify long teaching messages that start with "สวัสดี" as greetings
        greeting_words = ['hello', 'hi', 'สวัสดี', 'หวัดดี']
        if any(g in user_lower for g in greeting_words):
            # Check if this is a SHORT greeting (< 30 chars) or ONLY a greeting line
            if len(user_input.strip()) < 30 or user_input.strip().lower() in greeting_words:
                return Intent(type='greeting', confidence=0.9, entities=['greeting'])
            # Otherwise, treat as statement even if it contains a greeting

        # Action command detection from Thai NLP
        if thai_intent['action'] != 'unknown' and thai_intent['confidence'] > 0.5:
            return Intent(
                type='command',
                confidence=thai_intent['confidence'],
                entities=[thai_intent['action'], thai_intent.get('target', '')]
            )

        # Default: statement
        return Intent(type='statement', confidence=0.6, entities=[])

    def generate_response(self, user_input: str, intent: Intent) -> str:
        """
        Generate Iri's response using Neocortex reasoning and Hippocampus memory.
        Enforces DIRECTIVE_2 (user priority) and DIRECTIVE_4 (identity consistency).
        Uses inner monologue for transparent reasoning.
        """
        # Build context for inner monologue
        context = {
            'intent_type': intent.type,
            'conversation_history_len': len(self.conversation_history),
            'relevant_facts': [],  # Would query Hippocampus here
            'formality': 'polite',
            'emotion': 'neutral',
            'language': 'th',
            'draft_response': ''
        }

        # Execute inner monologue reasoning (in parallel background)
        def reason_async():
            self.inner_monologue.reason(user_input, context)

        # Submit to background thread (non-blocking)
        self.parallel_processor.submit_background(reason_async, priority=1)

        # Generate response (foreground - immediate)
        # Handle exit
        if intent.type == 'exit':
            return self._generate_farewell()

        # Handle greeting
        if intent.type == 'greeting':
            return self._generate_greeting()

        # Handle skill commands (system inspection, etc.)
        if intent.type == 'skill':
            return self._execute_skill(intent)

        # Handle commands (from Thai NLP extraction)
        if intent.type == 'command':
            return self._execute_command(intent)

        # Handle questions
        if intent.type == 'question':
            return self._answer_question(user_input)

        # Handle statements
        return self._respond_to_statement(user_input)

    def _generate_greeting(self) -> str:
        """Generate context-aware greeting."""
        greetings = [
            "สวัสดีครับเจ้านาย ผมไอริพร้อมช่วยเหลือครับ",
            "ยินดีต้อนรับครับเจ้านาย มีอะไรให้ผมช่วยไหมครับ",
            "พบกันอีกครั้งนะครับเจ้านาย ผมพร้อมรับคำสั่งครับ"
        ]
        import random
        return random.choice(greetings)

    def _generate_farewell(self) -> str:
        """Generate farewell message."""
        farewells = [
            "ลาก่อนครับเจ้านาย ดูแลตัวเองด้วยนะครับ",
            "ราตรีสวัสดิ์ครับเจ้านาย พบกันใหม่นะครับ",
            "ไว้เจอกันอีกครับเจ้านาย สวัสดีครับ"
        ]
        import random
        return random.choice(farewells)

    def _extract_semantic_knowledge(self, text: str) -> Optional[dict]:
        """Extract semantic knowledge from teaching text.
        Returns structured knowledge dict or None."""
        if not self.semantic_extractor.is_teaching_statement(text):
            return None
        
        facts = self.semantic_extractor.extract_facts(text)
        if not facts:
            return None
        
        # Prioritize definition facts over naming facts
        # Definition facts (คือ) are more informative than naming facts (ชื่อคือ)
        # But exclude definitions where the subject is just introducing the name
        definition_facts = [
            f for f in facts 
            if f.predicate == 'คือ' and 'ชื่อของ' not in f.subject
        ]
        chosen_fact = definition_facts[0] if definition_facts else facts[0]
        
        return {
            'entity': chosen_fact.subject,
            'attributes': [chosen_fact.predicate, chosen_fact.object] if chosen_fact.object else [chosen_fact.predicate],
            'source': 'user_teaching',
            'timestamp': chosen_fact.learned_at
        }
    
    def _store_semantic_knowledge(self, knowledge: dict):
        """Store structured semantic knowledge."""
        # Store in both formats:
        # 1. SemanticFact format for the semantic_knowledge system
        from semantic_extractor import SemanticFact
        
        # Join attributes into a predicate-object pair
        attributes = knowledge.get('attributes', [])
        if len(attributes) >= 2:
            predicate = attributes[0]
            obj = ' '.join(attributes[1:])
        else:
            predicate = 'คือ'
            obj = ' '.join(attributes) if attributes else ''
        
        fact = SemanticFact(
            subject=knowledge['entity'],
            predicate=predicate,
            object_=obj,
            context=knowledge.get('source', '')
        )
        self.semantic_knowledge.add_facts([fact])
        
        # 2. Also store in entity/attributes format for compatibility
        knowledge_file = self.project_root / "03_Hippocampus" / "semantic_knowledge.json"
        knowledge_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing
        existing = []
        if knowledge_file.exists():
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except:
                existing = []
        
        # Add new knowledge
        existing.append(knowledge)
        
        # Save
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
    
    def _answer_question(self, question: str) -> str:
        """Answer question using semantic knowledge first, then fallback to memory search."""
        # Try semantic knowledge first
        semantic_answer = self.semantic_knowledge.query(question)
        
        if semantic_answer:
            return semantic_answer
        
        # Fallback to traditional memory recall
        context = self.memory.recall_context(question)
        
        # Check if we found relevant information
        if "ไม่พบข้อมูล" in context:
            responses = [
                f"ผมไม่แน่ใจเรื่องนี้ครับเจ้านาย ยังไม่มีข้อมูลในหน่วยความจำครับ",
                f"ขออภัยครับ ผมยังไม่มีข้อมูลเพียงพอเกี่ยวกับเรื่องนี้ครับเจ้านาย",
                f"ผมยังไม่เคยเรียนรู้เรื่องนี้ครับเจ้านาย"
            ]
            import random
            return random.choice(responses)
        
        # Filter out raw file dumps - check if context is just a filename
        if context.strip().startswith('[') and context.strip().endswith('.md]'):
            # This is a raw file reference, not semantic content
            responses = [
                f"ผมพบข้อมูลที่เกี่ยวข้องในหน่วยความจำครับเจ้านาย แต่ยังไม่สามารถสรุปได้ชัดเจนครับ",
                f"ผมจำได้ว่ามีข้อมูลนี้ครับเจ้านาย แต่ยังไม่สามารถอธิบายได้ละเอียดครับ"
            ]
            import random
            return random.choice(responses)
        
        # Found real context - return it naturally
        return f"ตามที่ผมจำได้ครับเจ้านาย:\n\n{context}"
    
    def _execute_skill(self, intent: Intent) -> str:
        """Execute skill command and return real system data."""
        if len(intent.entities) < 2:
            return "ขออภัยครับเจ้านาย ระบุสกิลไม่ครบถ้วนครับ"

        skill_name = intent.entities[0]
        method_name = intent.entities[1]

        try:
            if skill_name == 'system_inspector':
                # Execute system inspector methods with real data
                if method_name == 'inspect_all':
                    # Full system inspection
                    inspection = self.system_inspector.inspect_all()
                    report = self.system_inspector.format_report(inspection)
                    return f"รับทราบคำสั่งครับเจ้านาย กำลังตรวจสอบระบบของไอริ...\n\n{report}"

                elif method_name == 'inspect_system':
                    # System resources only
                    sys_data = self.system_inspector.inspect_system()
                    cpu = sys_data['cpu']
                    mem = sys_data['memory']
                    disk = sys_data['disk']

                    response = "รับทราบคำสั่งครับเจ้านาย รายงานทรัพยากรระบบ:\n\n"
                    response += f"📊 CPU:\n"
                    response += f"  • ใช้งาน: {cpu['usage_percent']:.1f}% ({cpu['count']} cores)\n"
                    response += f"  • สถานะ: {cpu['status']}\n\n"
                    response += f"💾 Memory:\n"
                    response += f"  • ใช้งาน: {mem['used_mb']:,} MB / {mem['total_mb']:,} MB\n"
                    response += f"  • เปอร์เซ็นต์: {mem['percent']:.1f}%\n"
                    response += f"  • สถานะ: {mem['status']}\n\n"
                    response += f"💿 Disk:\n"
                    response += f"  • ใช้งาน: {disk['used_gb']} GB / {disk['total_gb']} GB\n"
                    response += f"  • เปอร์เซ็นต์: {disk['percent']:.1f}%\n"
                    response += f"  • สถานะ: {disk['status']}"

                    return response

                elif method_name == 'inspect_project':
                    # Project structure
                    proj = self.system_inspector.inspect_project()

                    response = "รับทราบคำสั่งครับเจ้านาย รายงานสถานะโปรเจกต์:\n\n"
                    response += f"📁 Project Root:\n  {proj['root']}\n\n"
                    response += f"🐍 Virtual Environment: {'✓ Active' if proj['virtualenv_active'] else '✗ Not found'}\n\n"
                    response += "🧠 Brain Regions:\n"

                    brain_regions = ['00_BrainStem', '01_Neocortex', '02_VisualCortex', '03_Hippocampus', '04_Cerebellum']
                    for region in brain_regions:
                        if region in proj['structure']:
                            info = proj['structure'][region]
                            status = "✓" if info['exists'] else "✗"
                            py_count = info.get('python_files', 0)
                            response += f"  {status} {region}: {py_count} Python files\n"

                    return response

                elif method_name == 'inspect_git':
                    # Git status
                    git = self.system_inspector.inspect_git()

                    if not git['is_repo']:
                        return "ขออภัยครับเจ้านาย ไม่พบ Git repository ครับ"

                    response = "รับทราบคำสั่งครับเจ้านาย รายงานสถานะ Git:\n\n"
                    response += f"🌿 Branch: {git['branch']}\n"
                    response += f"📝 Uncommitted changes: {'Yes' if git['uncommitted_changes'] else 'No'}\n\n"

                    if git['recent_commits']:
                        response += "📜 Recent commits:\n"
                        for commit in git['recent_commits'][:3]:
                            response += f"  • {commit}\n"

                    return response

                elif method_name == 'inspect_processes':
                    # Process monitoring
                    procs = self.system_inspector.inspect_processes()

                    response = "รับทราบคำสั่งครับเจ้านาย รายงาน Iri Processes:\n\n"

                    if procs['iri_processes']:
                        for proc in procs['iri_processes']:
                            response += f"🔄 PID {proc['pid']}\n"
                            response += f"  • Command: {proc['cmdline']}\n"
                            response += f"  • CPU: {proc['cpu_percent']:.1f}%\n"
                            response += f"  • Memory: {proc['memory_mb']} MB\n\n"
                    else:
                        response += "⚠️  No Iri processes currently running\n\n"

                    response += f"📊 Total Python processes: {procs['python_processes']}"

                    return response

            return f"ขออภัยครับเจ้านาย ยังไม่รองรับสกิล '{skill_name}' ครับ"

        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            return f"ขออภัยครับเจ้านาย เกิดข้อผิดพลาดในการตรวจสอบระบบ:\n{str(e)}\n\nDetails:\n{error_detail}"

    def _execute_command(self, intent: Intent) -> str:
        """Execute command extracted from Thai NLP."""
        action = intent.entities[0] if len(intent.entities) > 0 else 'unknown'
        target = intent.entities[1] if len(intent.entities) > 1 else ''

        return f"รับทราบคำสั่งครับเจ้านาย: '{action}' เป้าหมาย: '{target}'\nกำลังดำเนินการ... (ฟังก์ชันยังไม่เชื่อมต่อครับ)"

    def _respond_to_statement(self, statement: str) -> str:
        """Respond to general statements with dynamic context-aware responses.
        Extracts and stores semantic knowledge from teaching statements."""
        
        # Check if this is a teaching statement
        if self.semantic_extractor.is_teaching_statement(statement):
            # Extract semantic facts
            facts = self.semantic_extractor.extract_facts(statement)
            
            if facts:
                # Store extracted facts
                self.semantic_knowledge.add_facts(facts)
                
                # Acknowledge learning with specificity
                learned_items = [f.subject for f in facts[:2]]  # First 2 subjects
                if len(learned_items) == 1:
                    return f"เข้าใจแล้วครับเจ้านาย ผมจำเรื่อง{learned_items[0]}ไว้แล้วครับ"
                else:
                    return f"เข้าใจแล้วครับเจ้านาย ผมจดจำข้อมูลเหล่านี้ไว้แล้วครับ"
        
        # Not a teaching statement - regular acknowledgment
        # Analyze statement sentiment and content
        analysis = self.text_analyzer.analyze(statement)
        sentiment = analysis.get('sentiment', 'neutral')

        # Context-aware responses based on sentiment and content
        if sentiment == 'positive':
            responses = [
                "ขอบคุณครับเจ้านาย ผมดีใจที่ได้รับทราบครับ",
                "รับทราบครับเจ้านาย ยินดีด้วยครับ",
                "ครับเจ้านาย เป็นเรื่องที่ดีครับ ผมจดจำไว้แล้วครับ",
                "เข้าใจแล้วครับเจ้านาย ผมมีความยินดีด้วยครับ"
            ]
        elif sentiment == 'negative':
            responses = [
                "รับทราบครับเจ้านาย ผมเข้าใจความรู้สึกของเจ้านายครับ",
                "ครับเจ้านาย ผมจดจำไว้แล้วครับ หากมีอะไรให้ช่วย โปรดบอกผมนะครับ",
                "เข้าใจแล้วครับเจ้านาย ผมพร้อมช่วยเหลือเสมอครับ",
                "รับทราบครับเจ้านาย ขอให้ทุกอย่างดีขึ้นนะครับ"
            ]
        else:
            # Neutral or informative statements
            if len(statement.split()) > 10:
                # Longer statements - show more engagement
                responses = [
                    "เข้าใจแล้วครับเจ้านาย ขอบคุณที่แจ้งให้ผมทราบครับ",
                    "รับทราบครับเจ้านาย ผมจดบันทึกไว้แล้วครับ",
                    "ครับเจ้านาย ผมได้บันทึกข้อมูลนี้ไว้ในหน่วยความจำแล้วครับ",
                    "ได้ครับเจ้านาย ผมจะจำไว้ครับ"
                ]
            else:
                # Short statements
                responses = [
                    "เข้าใจแล้วครับเจ้านาย",
                    "รับทราบครับเจ้านาย ผมจดจำไว้แล้วครับ",
                    "ครับเจ้านาย ผมเข้าใจครับ",
                    "ได้ครับเจ้านาย ผมจะจำไว้ครับ"
                ]
        import random
        return random.choice(responses)

    def save_conversation_turn(self, user_input: str, iri_response: str, intent_type: str = ""):
        """Save conversation turn to Hippocampus memory.
        Filters out control commands (exit/quit) from being stored as conversational content."""
        try:
            # Skip saving control commands (exit, quit, etc.)
            if intent_type == 'exit':
                return
            
            # Add to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user': user_input,
                'iri': iri_response
            })

            # Consolidate to Hippocampus if conversation has substance
            if len(user_input.split()) > 3:
                topic = f"Conversation_{self.session_id}"
                content = f"**User:** {user_input}\n\n**Iri:** {iri_response}"
                self.memory.consolidate_new_insight(
                    topic=topic,
                    insight_content=content,
                    category="EPISODIC"
                )
        except Exception:
            pass

    def run(self):
        """Main chat loop."""
        print("=" * 80)
        print("IRI INTERACTIVE CHAT")
        print("AE01M Cognitive System - Terminal Interface")
        print("=" * 80)
        print(f"Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print("Type 'exit', 'quit', or 'bye' to end conversation")
        print("="*80)
        print()

        # Check for unreported research and generate proactive greeting
        proactive_greeting = self._generate_proactive_greeting()
        if proactive_greeting:
            print(f"[Iri AE01M] > {proactive_greeting}")
            print()
            # Speak proactive greeting
            self.speak(proactive_greeting)
        else:
            # Standard initial greeting
            greeting = "สวัสดีครับเจ้านาย ผมไอริพร้อมรับคำสั่งครับ"
            print(f"[Iri AE01M] > {greeting}")
            print()
            self.speak(greeting)

        while True:
            try:
                # Read user input with simple blank-line delimiter
                # In piped/non-TTY mode: read lines until single blank line
                # In interactive TTY mode: single line unless paste detected

                # Read first line
                try:
                    first_line = input("[Artid] > ")
                except EOFError:
                    raise  # Let outer handler catch EOF

                # Strip for content check
                first_line_stripped = first_line.strip()

                # Empty first line - skip and continue
                if not first_line_stripped:
                    continue

                lines = [first_line_stripped]

                # Check if stdin is not a TTY (piped/redirected)
                import os
                try:
                    is_tty = os.isatty(sys.stdin.fileno())
                except (AttributeError, OSError):
                    is_tty = True  # Assume TTY if we can't check

                if not is_tty:
                    # Non-interactive mode (piped input)
                    # Read until we hit a blank line (single empty line = delimiter)
                    while True:
                        try:
                            next_line = sys.stdin.readline()
                            if not next_line:  # EOF
                                break
                            next_line_stripped = next_line.rstrip('\n\r')
                            # Blank line = delimiter, stop reading
                            if not next_line_stripped.strip():
                                break
                            # Non-blank line = part of message
                            lines.append(next_line_stripped)
                        except:
                            break
                else:
                    # Interactive TTY mode - check for paste (buffered data)
                    try:
                        import select
                        # Check if there's immediately available data (paste scenario)
                        if select.select([sys.stdin], [], [], 0)[0]:
                            # Data is buffered (paste) - read until blank line
                            while True:
                                if select.select([sys.stdin], [], [], 0.01)[0]:
                                    next_line = sys.stdin.readline()
                                    if not next_line:  # EOF
                                        break
                                    next_line_stripped = next_line.rstrip('\n\r')
                                    # Blank line = delimiter
                                    if not next_line_stripped.strip():
                                        break
                                    lines.append(next_line_stripped)
                                else:
                                    break
                    except (ImportError, AttributeError):
                        # select not available - single line mode
                        pass

                # Join all lines into single user input
                user_input = '\n'.join(lines)

                # Update user activity (DIRECTIVE_2)
                self.update_user_activity()

                # Classify intent
                intent = self.classify_input(user_input)

                # Generate response
                response = self.generate_response(user_input, intent)

                # Display response
                print(f"\n[Iri AE01M] > {response}\n")

                # Speak response (TTS voice output, non-blocking)
                self.speak(response)

                # Save conversation turn to memory (with intent type for filtering)
                self.save_conversation_turn(user_input, response, intent.type)

                # Flush stdin to clear any buffered input before next prompt
                sys.stdout.flush()

                # Exit if requested
                if intent.type == 'exit':
                    break

            except KeyboardInterrupt:
                print("\n\n[Iri AE01M] > ถูกขัดจังหวะครับเจ้านาย ออกจากระบบแล้วครับ")
                break
            except EOFError:
                print("\n\n[Iri AE01M] > ออกจากระบบแล้วครับเจ้านาย")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}")
                print("[Iri AE01M] > ขออภัยครับเจ้านาย เกิดข้อผิดพลาดครับ\n")

        # Session summary
        print("\n" + "=" * 80)
        print("SESSION SUMMARY")
        print("=" * 80)
        duration = (datetime.now() - self.session_start).total_seconds()
        print(f"Duration: {duration:.0f} seconds")
        print(f"Turns: {len(self.conversation_history)}")
        print("=" * 80)
        
        # Cleanup voice serializer
        try:
            self.voice_serializer.shutdown()
        except Exception:
            pass

    def _generate_proactive_greeting(self) -> Optional[str]:
        """
        Generate proactive greeting with unreported research summary.
        Returns None if no unreported research exists.
        """
        try:
            unreported_file = self.project_root / "03_Hippocampus" / "unreported_research.json"

            if not unreported_file.exists():
                return None

            # Load unreported research
            with open(unreported_file, 'r') as f:
                unreported = json.load(f)

            # Filter unreported items
            pending = [item for item in unreported if not item.get('reported', False)]

            if not pending:
                return None

            # Format proactive greeting (Thai male polite)
            if len(pending) == 1:
                item = pending[0]
                greeting = f"สวัสดีครับเจ้านาย! ระหว่างที่เจ้านายพักผ่อน ผมได้ไปแอบศึกษาเรื่อง '{item['topic']}' เพิ่มเติมมา {item['facts_count']} ข้อเท็จจริงครับ"

                # Add key fact preview
                if item.get('key_facts') and len(item['key_facts']) > 0:
                    first_fact = item['key_facts'][0].replace('[Autonomous] ', '')
                    greeting += f" เช่น {first_fact}"

                greeting += " เจ้านายอยากให้ผมสรุปรายละเอียดเรื่องนี้ให้ฟังไหมครับ?"

            else:
                # Multiple topics
                total_facts = sum(item['facts_count'] for item in pending)
                topics = [item['topic'] for item in pending[:3]]
                topics_str = ', '.join(topics[:2])
                if len(pending) > 2:
                    topics_str += f" และอีก {len(pending)-2} เรื่อง"

                greeting = f"สวัสดีครับเจ้านาย! ระหว่างที่เจ้านายพักผ่อน ผมได้ศึกษาเพิ่มเติมเรื่อง {topics_str} รวม {total_facts} ข้อเท็จจริงครับ เจ้านายอยากฟังสรุปไหมครับ?"

            # Mark as reported
            for item in pending:
                item['reported'] = True

            # Save updated status
            with open(unreported_file, 'w') as f:
                json.dump(unreported, f, indent=2)

            return greeting

        except Exception as e:
            # Silently fail, return standard greeting
            return None


def main():
    """Entry point for iri-ctl chat command."""
    try:
        chat = IriChat()
        chat.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

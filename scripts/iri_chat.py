#!/usr/bin/env python3
"""
Iri Interactive Chat Terminal
Real-time conversational interface with AE01M cognitive system.
"""
import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import Neocortex and Hippocampus
try:
    sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))
    sys.path.insert(0, str(PROJECT_ROOT / "03_Hippocampus"))
    sys.path.insert(0, str(PROJECT_ROOT / "04_Cerebellum"))
    
    from executive_core import KnowledgeGraph, Intent
    from memory_store import HippocampusMemory
    from core_directives import CoreDirectives
    from nlp_thai_lexicon import get_thai_lexicon
    from skills import get_system_inspector, get_text_analyzer
    from voice_synthesis import speak_aloud  # TTS voice output
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
        
        # TTS voice output (enabled by default)
        self.voice_enabled = True
        try:
            # Test TTS availability
            from voice_synthesis import default_synthesizer
            self.voice_available = True
            print("✓ Voice synthesis enabled")
        except Exception as e:
            self.voice_available = False
            print(f"⚠️  Voice synthesis unavailable: {e}")
            print("   Continuing in text-only mode")
    
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
        Speak text using TTS voice synthesis (non-blocking).
        Plays audio in background thread so it doesn't block user input.
        """
        if not self.voice_enabled or not self.voice_available:
            return
        
        try:
            # Use non-blocking speak (block=False)
            import threading
            threading.Thread(target=lambda: speak_aloud(text, block=False), daemon=True).start()
        except Exception as e:
            # Silently fail - don't disrupt chat flow
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
        
        # Command detection
        if any(cmd in user_lower for cmd in ['exit', 'quit', 'bye', 'ออก', 'ลาก่อน']):
            return Intent(type='exit', confidence=1.0, entities=['exit'])
        
        # Question detection
        if any(q in user_lower for q in ['?', 'what', 'why', 'how', 'when', 'who', 
                                          'อะไร', 'ทำไม', 'อย่างไร', 'เมื่อไหร่']):
            return Intent(type='question', confidence=0.8, entities=thai_intent.get('entities', {}).get('object', []))
        
        # Greeting detection
        if any(g in user_lower for g in ['hello', 'hi', 'สวัสดี', 'หวัดดี']):
            return Intent(type='greeting', confidence=0.9, entities=['greeting'])
        
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
        """
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
    
    def _answer_question(self, question: str) -> str:
        """Answer question using Hippocampus memory recall."""
        # Search memory for relevant context
        context = self.memory.recall_context(question)
        
        # Check if we found relevant information
        if "ไม่พบข้อมูล" in context:
            responses = [
                f"ผมไม่แน่ใจเรื่องนี้ครับเจ้านาย กำลังค้นหาข้อมูลในหน่วยความจำ...\n{context}",
                f"ขออภัยครับ ผมยังไม่มีข้อมูลเพียงพอเกี่ยวกับเรื่องนี้ครับเจ้านาย",
                f"ให้ผมลองค้นหาให้นะครับเจ้านาย...\n{context}"
            ]
            import random
            return random.choice(responses)
        
        # Found context
        return f"ตามที่ผมค้นหาในหน่วยความจำครับเจ้านาย:\n\n{context}"
    
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
        """Respond to general statements with dynamic context-aware responses."""
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
    
    def save_conversation_turn(self, user_input: str, iri_response: str):
        """Save conversation turn to Hippocampus memory."""
        try:
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
        print("=" * 80)
        print()
        
        # Initial greeting
        print("[Iri AE01M] > สวัสดีครับเจ้านาย ผมไอริพร้อมรับคำสั่งครับ")
        print()
        
        while True:
            try:
                # User input with prompt
                user_input = input("[Artid] > ").strip()
                
                if not user_input:
                    continue
                
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
                
                # Save conversation turn to memory
                self.save_conversation_turn(user_input, response)
                
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

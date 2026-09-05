from .helpers import format_uptime, format_memory_content, memory_type_color
from .memory_panel import MemoryPanel
from .runtime_snapshot import RuntimeSnapshot

import math
import tkinter as tk
from tkinter import ttk

from runtime.runtime import TranscendingRuntime


# ============================================================
# AE01M — Obsidian-like Desktop Cognitive Console
# ============================================================

APP_TITLE = "AE01M — The Transcending Form"

# ------------------------------------------------------------
# Obsidian Dark Desktop Theme Tokens
# ------------------------------------------------------------
BG_APP = "#16161a"          # Obsidian primary background
BG_SIDEBAR = "#1e1e24"      # Navigation sidebar background
BG_SURFACE = "#22222a"      # Card/workspace surface
BG_SURFACE_HOVER = "#2a2a34"# Hover surface
BG_TAB_ACTIVE = "#262630"   # Active tab header
BG_STATUS = "#141417"       # Bottom status bar

BORDER = "#30303c"          # Subtle border
BORDER_MUTED = "#262630"    # Even subtler divider

TEXT = "#dcddde"            # Primary text
TEXT_SECONDARY = "#9da0a6"  # Secondary text
TEXT_MUTED = "#6f737d"      # Muted labels / hotkeys
ACCENT_PURPLE = "#7c3aed"   # Obsidian-like purple accent
ACCENT_PURPLE_HOVER = "#8b5cf6"
CYAN = "#38bdf8"
GREEN = "#4ade80"
YELLOW = "#facc15"
RED = "#f87171"
WHITE = "#ffffff"


class AE01MApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("1560x940")
        self.minsize(1200, 720)
        self.configure(bg=BG_APP)

        self.runtime = TranscendingRuntime()
        self.runtime_snapshot = RuntimeSnapshot(self.runtime)
        self.dashboard_snapshot = {}

        self.active_tab = "Chat"
        self.tab_buttons = {}
        self.tab_frames = {}

        self._configure_styles()
        self._build_ui()

        # Keyboard shortcuts
        self.bind("<Control-k>", lambda e: self.search_entry.focus_set())
        self.bind("<Control-K>", lambda e: self.search_entry.focus_set())
        for num, name in enumerate(["Chat", "Memory", "Brain", "Research", "Learning", "System"], start=1):
            self.bind(f"<Control-Key-{num}>", lambda e, n=name: self._select_tab(n))
            self.bind(f"<Control-{num}>", lambda e, n=name: self._select_tab(n))

        self.after(1000, self._refresh_runtime)

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "TScrollbar",
            background=BG_SURFACE,
            troughcolor=BG_APP,
            bordercolor=BORDER,
            arrowcolor=TEXT_MUTED,
            relief="flat",
        )

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_top_bar()
        self._build_body_area()
        self._build_status_bar()

    # ------------------------------------------------------------
    # Top Obsidian Command / Title Bar
    # ------------------------------------------------------------
    def _build_top_bar(self):
        top_bar = tk.Frame(self, bg=BG_STATUS, height=44, bd=0, highlightthickness=1, highlightbackground=BORDER)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_propagate(False)

        top_bar.grid_columnconfigure(1, weight=1)

        # Brand / App Icon
        brand_frame = tk.Frame(top_bar, bg=BG_STATUS)
        brand_frame.grid(row=0, column=0, padx=16, sticky="w")

        icon_lbl = tk.Label(brand_frame, text="◆", bg=BG_STATUS, fg=ACCENT_PURPLE, font=("TkDefaultFont", 13, "bold"))
        icon_lbl.pack(side="left", padx=(0, 6))

        brand_lbl = tk.Label(brand_frame, text="AE01M", bg=BG_STATUS, fg=TEXT, font=("TkDefaultFont", 11, "bold"))
        brand_lbl.pack(side="left")

        ver_lbl = tk.Label(brand_frame, text="v1.0.0-phase13", bg=BG_STATUS, fg=TEXT_MUTED, font=("TkDefaultFont", 8))
        ver_lbl.pack(side="left", padx=(6, 0))

        # Command / Search bar (Obsidian quick switcher style)
        search_frame = tk.Frame(top_bar, bg=BG_SIDEBAR, bd=0, highlightthickness=1, highlightbackground=BORDER)
        search_frame.grid(row=0, column=1, pady=6, padx=40, sticky="ew")

        search_icon = tk.Label(search_frame, text="🔍", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=("TkDefaultFont", 9))
        search_icon.pack(side="left", padx=(8, 4))

        self.search_entry = tk.Entry(
            search_frame,
            bg=BG_SIDEBAR,
            fg=TEXT,
            insertbackground=WHITE,
            relief="flat",
            bd=0,
            font=("TkDefaultFont", 9),
        )
        self.search_entry.insert(0, "Quick switcher or command... (Ctrl+K)")
        self.search_entry.bind("<FocusIn>", self._on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_search_focus_out)
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Right actions / indicators
        right_meta = tk.Frame(top_bar, bg=BG_STATUS)
        right_meta.grid(row=0, column=2, padx=16, sticky="e")

        self.autonomous_indicator = tk.Label(
            right_meta,
            text="● HUMAN GATED",
            bg=BG_STATUS,
            fg=YELLOW,
            font=("TkDefaultFont", 8, "bold"),
        )
        self.autonomous_indicator.pack(side="left", padx=(0, 12))

        sync_btn = tk.Button(
            right_meta,
            text="Sync Memory",
            command=self._manual_sync,
            relief="flat",
            bd=0,
            padx=10,
            pady=3,
            bg=BG_SURFACE,
            fg=TEXT_SECONDARY,
            activebackground=BG_SURFACE_HOVER,
            activeforeground=TEXT,
            font=("TkDefaultFont", 8),
            cursor="hand2",
        )
        sync_btn.pack(side="left")

    def _on_search_focus_in(self, event):
        if self.search_entry.get().startswith("Quick switcher"):
            self.search_entry.delete(0, "end")

    def _on_search_focus_out(self, event):
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "Quick switcher or command... (Ctrl+K)")

    # ------------------------------------------------------------
    # Main Body: Left Sidebar + Central Multi-tab Workspace + Right Inspector
    # ------------------------------------------------------------
    def _build_body_area(self):
        body = tk.Frame(self, bg=BG_APP)
        body.grid(row=1, column=0, sticky="nsew")

        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=0)  # Left sidebar
        body.grid_columnconfigure(1, weight=1)  # Main Workspace (tabs)
        body.grid_columnconfigure(2, weight=0)  # Right Properties panel

        self._build_left_sidebar(body)
        self._build_center_workspace(body)
        self._build_right_inspector(body)

    # ------------------------------------------------------------
    # Left Navigation Sidebar
    # ------------------------------------------------------------
    def _build_left_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_SIDEBAR, width=220, bd=0, highlightthickness=1, highlightbackground=BORDER)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Header
        lbl_head = tk.Label(sidebar, text="CORE NAVIGATION", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=("TkDefaultFont", 8, "bold"))
        lbl_head.pack(anchor="w", padx=16, pady=(16, 8))

        tabs = [
            ("Chat", "💬", "Ctrl+1"),
            ("Memory", "🕸", "Ctrl+2"),
            ("Brain", "🧠", "Ctrl+3"),
            ("Research", "🔬", "Ctrl+4"),
            ("Learning", "📚", "Ctrl+5"),
            ("System", "⚙", "Ctrl+6"),
        ]

        for name, icon, shortcut in tabs:
            btn_frame = tk.Frame(sidebar, bg=BG_SIDEBAR, cursor="hand2")
            btn_frame.pack(fill="x", padx=8, pady=2)

            btn = tk.Button(
                btn_frame,
                text=f"  {icon}  {name}",
                command=lambda n=name: self._select_tab(n),
                relief="flat",
                bd=0,
                anchor="w",
                bg=BG_SIDEBAR,
                fg=TEXT_SECONDARY,
                activebackground=BG_SURFACE_HOVER,
                activeforeground=TEXT,
                font=("TkDefaultFont", 9),
                cursor="hand2",
            )
            btn.pack(side="left", fill="x", expand=True, ipady=4)

            shortcut_lbl = tk.Label(btn_frame, text=shortcut, bg=BG_SIDEBAR, fg=TEXT_MUTED, font=("TkDefaultFont", 7))
            shortcut_lbl.pack(side="right", padx=(0, 8))

            self.tab_buttons[name] = (btn, btn_frame)

        # Sidebar Bottom Section: Active State Summary
        divider = tk.Frame(sidebar, bg=BORDER, height=1)
        divider.pack(fill="x", padx=12, pady=(20, 10))

        stage_box = tk.Frame(sidebar, bg=BG_SIDEBAR)
        stage_box.pack(fill="x", padx=16, pady=4)

        tk.Label(stage_box, text="DEVELOPMENT STAGE", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=("TkDefaultFont", 7, "bold")).pack(anchor="w")
        self.sidebar_stage_val = tk.Label(stage_box, text="NEWBORN", bg=BG_SIDEBAR, fg=CYAN, font=("TkDefaultFont", 9, "bold"))
        self.sidebar_stage_val.pack(anchor="w")

        tk.Label(stage_box, text="EXPERIENCE", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=("TkDefaultFont", 7, "bold"), pady=4).pack(anchor="w")
        self.sidebar_exp_val = tk.Label(stage_box, text="0 cycles", bg=BG_SIDEBAR, fg=TEXT, font=("TkDefaultFont", 9))
        self.sidebar_exp_val.pack(anchor="w")

    # ------------------------------------------------------------
    # Central Workspace with Tab Switching
    # ------------------------------------------------------------
    def _build_center_workspace(self, parent):
        workspace = tk.Frame(parent, bg=BG_APP)
        workspace.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)
        workspace.grid_rowconfigure(1, weight=1)
        workspace.grid_columnconfigure(0, weight=1)

        # Tab Header Bar (Obsidian editor tab bar)
        tab_bar = tk.Frame(workspace, bg=BG_APP, height=36)
        tab_bar.grid(row=0, column=0, sticky="ew")

        self.tab_header_btns = {}
        for tab_name in ("Chat", "Memory", "Brain", "Research", "Learning", "System"):
            t_btn = tk.Button(
                tab_bar,
                text=f"{tab_name}",
                command=lambda n=tab_name: self._select_tab(n),
                relief="flat",
                bd=0,
                padx=16,
                pady=6,
                bg=BG_APP,
                fg=TEXT_MUTED,
                activebackground=BG_TAB_ACTIVE,
                activeforeground=TEXT,
                font=("TkDefaultFont", 9),
                cursor="hand2",
            )
            t_btn.pack(side="left", padx=(0, 2))
            self.tab_header_btns[tab_name] = t_btn

        # Central container holding individual tab frames
        self.container = tk.Frame(workspace, bg=BG_SURFACE, bd=0, highlightthickness=1, highlightbackground=BORDER)
        self.container.grid(row=1, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Instantiate Tabs
        self.tab_frames["Chat"] = self._build_chat_tab(self.container)
        self.tab_frames["Memory"] = self._build_memory_tab(self.container)
        self.tab_frames["Brain"] = self._build_brain_tab(self.container)
        self.tab_frames["Research"] = self._build_research_tab(self.container)
        self.tab_frames["Learning"] = self._build_learning_tab(self.container)
        self.tab_frames["System"] = self._build_system_tab(self.container)

        self._select_tab("Chat")

    def _select_tab(self, name: str):
        self.active_tab = name

        # Update sidebar buttons
        for tab, (btn, frame) in self.tab_buttons.items():
            if tab == name:
                btn.configure(bg=BG_SURFACE_HOVER, fg=WHITE, font=("TkDefaultFont", 9, "bold"))
                frame.configure(bg=BG_SURFACE_HOVER)
            else:
                btn.configure(bg=BG_SIDEBAR, fg=TEXT_SECONDARY, font=("TkDefaultFont", 9))
                frame.configure(bg=BG_SIDEBAR)

        # Update top tab bar buttons
        for tab, btn in self.tab_header_btns.items():
            if tab == name:
                btn.configure(bg=BG_SURFACE, fg=TEXT, font=("TkDefaultFont", 9, "bold"))
            else:
                btn.configure(bg=BG_APP, fg=TEXT_MUTED, font=("TkDefaultFont", 9))

        # Switch visible frame
        for tab, frame in self.tab_frames.items():
            if tab == name:
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame.grid_forget()

    # ------------------------------------------------------------
    # Right Properties / Context Inspector
    # ------------------------------------------------------------
    def _build_right_inspector(self, parent):
        inspector = tk.Frame(parent, bg=BG_SIDEBAR, width=280, bd=0, highlightthickness=1, highlightbackground=BORDER)
        inspector.grid(row=0, column=2, sticky="nsew")
        inspector.grid_propagate(False)

        tk.Label(inspector, text="PROPERTIES & STATE", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=("TkDefaultFont", 8, "bold")).pack(anchor="w", padx=16, pady=(16, 12))

        fields = [
            ("Identity Stage", "stage_prop", "NEWBORN"),
            ("Self Awareness", "awareness_prop", "0.00"),
            ("Self Knowledge", "knowledge_prop", "0.00"),
            ("Active Goals", "goals_prop", "0"),
            ("Pending Intentions", "intentions_prop", "0"),
            ("Episodic Memory", "episodic_prop", "0"),
            ("Semantic Memory", "semantic_prop", "0"),
            ("Working Memory", "working_prop", "0"),
            ("Neural Populations", "neural_prop", "Allocated: 0"),
        ]

        self.prop_labels = {}
        for title, key, default_val in fields:
            box = tk.Frame(inspector, bg=BG_SIDEBAR)
            box.pack(fill="x", padx=16, pady=4)

            tk.Label(box, text=title, bg=BG_SIDEBAR, fg=TEXT_SECONDARY, font=("TkDefaultFont", 8)).pack(anchor="w")
            lbl_val = tk.Label(box, text=default_val, bg=BG_SIDEBAR, fg=TEXT, font=("TkDefaultFont", 8, "bold"))
            lbl_val.pack(anchor="w")
            self.prop_labels[key] = lbl_val

        # Bottom Safety / Gateway box
        divider = tk.Frame(inspector, bg=BORDER, height=1)
        divider.pack(fill="x", padx=16, pady=(16, 10))

        safety_box = tk.Frame(inspector, bg=BG_SIDEBAR)
        safety_box.pack(fill="x", padx=16, pady=4)

        tk.Label(safety_box, text="SAFETY BOUNDARY", bg=BG_SIDEBAR, fg=TEXT_MUTED, font=("TkDefaultFont", 8, "bold")).pack(anchor="w")
        self.safety_status_lbl = tk.Label(safety_box, text="Cognitive Safety Gate: ACTIVE", bg=BG_SIDEBAR, fg=GREEN, font=("TkDefaultFont", 8))
        self.safety_status_lbl.pack(anchor="w", pady=(2, 0))

    # ------------------------------------------------------------
    # Tab 1: Chat Workspace
    # ------------------------------------------------------------
    def _build_chat_tab(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=BG_SURFACE)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Editor-style Chat Display
        self.chat_text = tk.Text(
            frame,
            bg=BG_SURFACE,
            fg=TEXT,
            insertbackground=WHITE,
            relief="flat",
            bd=0,
            padx=20,
            pady=16,
            font=("TkDefaultFont", 10),
            state="disabled",
            wrap="word",
        )
        self.chat_text.grid(row=0, column=0, sticky="nsew")

        # Input dock
        input_bar = tk.Frame(frame, bg=BG_APP, padx=16, pady=12, highlightthickness=1, highlightbackground=BORDER)
        input_bar.grid(row=1, column=0, sticky="ew")
        input_bar.grid_columnconfigure(0, weight=1)

        self.chat_entry = tk.Entry(
            input_bar,
            bg=BG_SURFACE,
            fg=TEXT,
            insertbackground=WHITE,
            relief="flat",
            bd=0,
            font=("TkDefaultFont", 10),
        )
        self.chat_entry.grid(row=0, column=0, sticky="ew", ipady=8, padx=(0, 10))
        self.chat_entry.insert(0, "Message AE01M...")
        self.chat_entry.bind("<FocusIn>", lambda e: self.chat_entry.delete(0, "end") if self.chat_entry.get().startswith("Message") else None)
        self.chat_entry.bind("<Return>", lambda e: self._send_message())

        send_btn = tk.Button(
            input_bar,
            text="Send",
            command=self._send_message,
            relief="flat",
            bd=0,
            padx=20,
            pady=6,
            bg=ACCENT_PURPLE,
            fg=WHITE,
            activebackground=ACCENT_PURPLE_HOVER,
            activeforeground=WHITE,
            font=("TkDefaultFont", 9, "bold"),
            cursor="hand2",
        )
        send_btn.grid(row=0, column=1)

        return frame

    # ------------------------------------------------------------
    # Tab 2: Memory Graph
    # ------------------------------------------------------------
    def _build_memory_tab(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=BG_SURFACE)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.memory_panel_controller = MemoryPanel(
            parent=frame,
            runtime=self.runtime,
            panel_builder=lambda p: tk.Frame(p, bg=BG_SURFACE),
            panel_header_builder=lambda p, title, subtitle, color=None: None,
            colors={
                "SURFACE": BG_SURFACE,
                "SURFACE_2": BG_APP,
                "SURFACE_3": BG_SURFACE_HOVER,
                "BORDER": BORDER,
                "BORDER_LIGHT": BORDER_MUTED,
                "TEXT": TEXT,
                "TEXT_SECONDARY": TEXT_SECONDARY,
                "TEXT_MUTED": TEXT_MUTED,
                "CYAN": CYAN,
                "YELLOW": YELLOW,
            },
        )
        mem_view = self.memory_panel_controller.build()
        mem_view.grid(row=0, column=0, sticky="nsew")

        return frame

    # ------------------------------------------------------------
    # Tab 3: Brain Substrate Inspector
    # ------------------------------------------------------------
    def _build_brain_tab(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=BG_SURFACE, padx=24, pady=20)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="Neural Substrate Monitor", bg=BG_SURFACE, fg=TEXT, font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 16))

        info_text = (
            "Substrate Foundation: LIF Neuron Vectors + Neuron Populations\n"
            "Regions: Hippocampus, Motor Cortex\n"
            "Synaptic Transport: Fixed float32 weights & propagation cycles\n"
            "Plasticity: Co-activity dependent weight adaptation\n"
            "State Boundary: Detached NeuralState snapshots"
        )
        tk.Label(frame, text=info_text, bg=BG_SURFACE, fg=TEXT_SECONDARY, font=("TkDefaultFont", 10), justify="left").grid(row=1, column=0, sticky="nw")

        self.brain_stats_label = tk.Label(frame, text="Allocating populations...", bg=BG_SURFACE, fg=CYAN, font=("TkDefaultFont", 10), justify="left")
        self.brain_stats_label.grid(row=2, column=0, sticky="nw", pady=(16, 0))

        return frame

    # ------------------------------------------------------------
    # Tab 4: Research Dashboard
    # ------------------------------------------------------------
    def _build_research_tab(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=BG_SURFACE, padx=24, pady=20)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="Research Execution Console", bg=BG_SURFACE, fg=TEXT, font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 16))

        desc = (
            "Research Subsystem: Numerical Hypotheses & Web Ingestion\n"
            "Evidence Trail: Persistent cycle history with dynamical evaluation\n"
            "Safety: Protected category gating before memory candidate creation"
        )
        tk.Label(frame, text=desc, bg=BG_SURFACE, fg=TEXT_SECONDARY, font=("TkDefaultFont", 10), justify="left").grid(row=1, column=0, sticky="nw")

        return frame

    # ------------------------------------------------------------
    # Tab 5: Learning & Practice Subsystem
    # ------------------------------------------------------------
    def _build_learning_tab(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=BG_SURFACE, padx=24, pady=20)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="Learning & Practice Subsystem", bg=BG_SURFACE, fg=TEXT, font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 16))

        desc = (
            "Learning Loop: Experience → Practice → Evaluation → Feedback → Update\n"
            "Practice Verifiers: Exact match & Numerical with tolerance\n"
            "Integration: Successful practice updates episodic memory and syncs hippocampus"
        )
        tk.Label(frame, text=desc, bg=BG_SURFACE, fg=TEXT_SECONDARY, font=("TkDefaultFont", 10), justify="left").grid(row=1, column=0, sticky="nw")

        return frame

    # ------------------------------------------------------------
    # Tab 6: System & Diagnostics
    # ------------------------------------------------------------
    def _build_system_tab(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=BG_SURFACE, padx=24, pady=20)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="System Infrastructure & Guardrails", bg=BG_SURFACE, fg=TEXT, font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 16))

        self.sys_info_label = tk.Label(frame, text="Monitoring runtime...", bg=BG_SURFACE, fg=TEXT_SECONDARY, font=("TkDefaultFont", 10), justify="left")
        self.sys_info_label.grid(row=1, column=0, sticky="nw")

        return frame

    # ------------------------------------------------------------
    # Bottom Status Bar
    # ------------------------------------------------------------
    def _build_status_bar(self):
        bar = tk.Frame(self, bg=BG_STATUS, height=28, bd=0, highlightthickness=1, highlightbackground=BORDER)
        bar.grid(row=2, column=0, sticky="ew")
        bar.grid_propagate(False)

        self.status_left = tk.Label(bar, text="Ready", bg=BG_STATUS, fg=TEXT_MUTED, font=("TkDefaultFont", 8))
        self.status_left.pack(side="left", padx=16)

        self.status_right = tk.Label(bar, text="Memory: OK  |  Substrate: Online  |  Safety: Active", bg=BG_STATUS, fg=TEXT_MUTED, font=("TkDefaultFont", 8))
        self.status_right.pack(side="right", padx=16)

    # ------------------------------------------------------------
    # Dynamic Updates & Refresh
    # ------------------------------------------------------------
    def _send_message(self):
        text = self.chat_entry.get().strip()
        if not text or text.startswith("Message AE01M"):
            return

        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", f"\nUser\n{text}\n\n", "user_tag")
        self.chat_text.tag_config("user_tag", foreground=CYAN, font=("TkDefaultFont", 10, "bold"))
        self.chat_entry.delete(0, "end")

        cycle = self.runtime.cognitive_loop.process(text)

        if cycle.reasoning:
            self.chat_text.insert("end", f"AE01M\n{cycle.reasoning}\n\n", "agent_tag")
            self.chat_text.tag_config("agent_tag", foreground=TEXT, font=("TkDefaultFont", 10))
        else:
            self.chat_text.insert("end", f"AE01M\n[Observed: decision={cycle.decision}]\n\n", "agent_muted")
            self.chat_text.tag_config("agent_muted", foreground=TEXT_MUTED, font=("TkDefaultFont", 9, "italic"))

        self.chat_text.configure(state="disabled")
        self.chat_text.see("end")

        self._refresh_runtime()

    def _manual_sync(self):
        count = self.runtime.sync_brain_memory()
        self.status_left.configure(text=f"Synced {count} episodic items to Brain")
        self._refresh_runtime()

    def _refresh_runtime(self):
        try:
            snapshot = self.runtime_snapshot.capture()

            # Refresh Memory Panel
            self.memory_panel_controller.refresh(snapshot)

            # Refresh Properties
            identity_snap = snapshot.get("identity") if isinstance(snapshot.get("identity"), dict) else {}
            stage_str = str(identity_snap.get("stage", "NEWBORN"))
            exp_int = int(identity_snap.get("experience", 0))

            self.sidebar_stage_val.configure(text=stage_str)
            self.sidebar_exp_val.configure(text=f"{exp_int} cycles")

            self.prop_labels["stage_prop"].configure(text=stage_str)

            self_model = snapshot.get("self_model") if isinstance(snapshot.get("self_model"), dict) else {}
            self.prop_labels["awareness_prop"].configure(text=f"{float(self_model.get('self_awareness', 0.0)):.2f}")
            self.prop_labels["knowledge_prop"].configure(text=f"{float(self_model.get('self_knowledge', 0.0)):.2f}")
            self.prop_labels["goals_prop"].configure(text=str(len(self.runtime.goals)))
            self.prop_labels["intentions_prop"].configure(text=str(len(self.runtime.intentions)))

            mem = snapshot.get("memory") if isinstance(snapshot.get("memory"), dict) else {}
            self.prop_labels["episodic_prop"].configure(text=str(len(mem.get("episodic", []))))
            self.prop_labels["semantic_prop"].configure(text=str(len(mem.get("semantic", []))))
            self.prop_labels["working_prop"].configure(text=str(len(mem.get("working", []))))

            brain_stats = self.runtime.brain.stats()
            hipp = brain_stats.get("hippocampus")
            motor = brain_stats.get("motor_cortex")

            hipp_allocated = getattr(hipp, "allocated_neurons", 0)
            hipp_chunks = getattr(hipp, "allocated_chunks", 0)
            motor_allocated = getattr(motor, "allocated_neurons", 0)
            motor_chunks = getattr(motor, "allocated_chunks", 0)

            self.prop_labels["neural_prop"].configure(text=f"Hipp: {hipp_allocated} / Motor: {motor_allocated}")

            self.brain_stats_label.configure(
                text=(
                    f"Total Neurons: {brain_stats.get('total_neurons', 0):,}\n"
                    f"Hippocampus Allocated: {hipp_allocated} / Chunks: {hipp_chunks}\n"
                    f"Motor Cortex Allocated: {motor_allocated} / Chunks: {motor_chunks}"
                )
            )

            self.status_left.configure(text=f"Active Stage: {stage_str} | Cycles: {exp_int}")

        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.status_left.configure(text=f"Error: {exc}")

        self.after(3000, self._refresh_runtime)


def main():
    app = AE01MApp()
    app.mainloop()


if __name__ == "__main__":
    main()

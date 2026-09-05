import math
import tkinter as tk

from .helpers import (
    format_memory_content,
    memory_type_color,
)


class MemoryPanel:
    """Memory dashboard panel backed by the real AE01M MemoryGraph."""

    def __init__(
        self,
        parent,
        runtime,
        panel_builder,
        panel_header_builder,
        colors,
    ):
        self.parent = parent
        self.runtime = runtime
        self._panel = panel_builder
        self._panel_header = panel_header_builder

        for name, value in colors.items():
            setattr(self, name, value)

        self.memory_metrics = {}
        self.graph_canvas = None
        self.recent_memory_label = None

        # Pulse state is driven only by real MemoryGraph activity.
        self.active_edges = set()
        self.pulse_progress = 0.0
        self.pulse_job = None
        self.node_positions = {}
        self.graph_nodes = {}
        self.graph_edges = {}

    def build(self):
        panel = self._panel(self.parent)

        self._panel_header(
            panel,
            "Memory",
            "Live",
            self.CYAN,
        )

        body = tk.Frame(
            panel,
            bg=self.SURFACE,
        )

        body.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10,
        )

        body.grid_rowconfigure(1, weight=1)
        body.grid_columnconfigure(0, weight=1)

        self._build_metrics(body)
        self._build_graph(body)
        self._build_recent_memories(body)

        return panel

    def _build_metrics(self, body):
        metrics = tk.Frame(
            body,
            bg=self.SURFACE,
        )

        metrics.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )

        for index in range(4):
            metrics.grid_columnconfigure(
                index,
                weight=1,
                uniform="memory_metric",
            )

        metric_names = (
            ("Nodes", "nodes"),
            ("Connections", "connections"),
            ("Experiences", "experiences"),
            ("Last Update", "last_update"),
        )

        for index, (label, key) in enumerate(metric_names):
            card = tk.Frame(
                metrics,
                bg=self.SURFACE_2,
                highlightbackground=self.BORDER,
                highlightthickness=1,
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=(
                    0 if index == 0 else 3,
                    3,
                ),
            )

            tk.Label(
                card,
                text=label.upper(),
                bg=self.SURFACE_2,
                fg=self.TEXT_MUTED,
                font=("TkDefaultFont", 7),
            ).pack(pady=(8, 1))

            value = tk.Label(
                card,
                text="—",
                bg=self.SURFACE_2,
                fg=self.TEXT,
                font=("TkDefaultFont", 10, "bold"),
            )

            value.pack(pady=(0, 8))

            self.memory_metrics[key] = value

    def _build_graph(self, body):
        graph = tk.Frame(
            body,
            bg=self.SURFACE_2,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        graph.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        graph.grid_rowconfigure(0, weight=1)
        graph.grid_columnconfigure(0, weight=1)

        self.graph_canvas = tk.Canvas(
            graph,
            bg=self.SURFACE_2,
            highlightthickness=0,
            bd=0,
        )

        self.graph_canvas.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.graph_canvas.bind(
            "<Configure>",
            lambda event: self.draw_graph(),
        )

    def _build_recent_memories(self, body):
        recent = tk.Frame(
            body,
            bg=self.SURFACE,
        )

        recent.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(10, 0),
        )

        tk.Label(
            recent,
            text="RECENT MEMORIES",
            bg=self.SURFACE,
            fg=self.TEXT_MUTED,
            font=("TkDefaultFont", 7, "bold"),
        ).pack(anchor="w")

        self.recent_memory_label = tk.Label(
            recent,
            text="No recent memory data",
            bg=self.SURFACE,
            fg=self.TEXT_SECONDARY,
            anchor="w",
            justify="left",
            wraplength=400,
            font=("TkDefaultFont", 8),
        )

        self.recent_memory_label.pack(
            anchor="w",
            pady=(5, 8),
        )

        button = tk.Button(
            recent,
            text="View Full Memory Graph  →",
            bg=self.SURFACE_3,
            fg=self.CYAN,
            activebackground=self.BORDER_LIGHT,
            activeforeground=self.TEXT,
            relief="flat",
            bd=0,
            pady=6,
            cursor="hand2",
            font=("TkDefaultFont", 8, "bold"),
        )

        button.pack(fill="x")

    def draw_graph(self, nodes=None, edges=None, activity=None):
        canvas = self.graph_canvas

        if canvas is None:
            return

        canvas.delete("all")

        if nodes is None:
            nodes = self.graph_nodes
        else:
            self.graph_nodes = nodes

        if edges is None:
            edges = self.graph_edges
        else:
            self.graph_edges = edges

        if activity is None:
            activity = {}

        nodes = list(nodes.items())
        edges = list(edges.values())

        active_nodes = set(activity.get("nodes", []))
        active_edges = {
            tuple(edge)
            for edge in activity.get("edges", [])
        }

        width = max(canvas.winfo_width(), 300)
        height = max(canvas.winfo_height(), 300)

        if not nodes:
            canvas.create_text(
                width // 2,
                height // 2 - 10,
                text="No memory nodes",
                fill=self.TEXT_SECONDARY,
                font=("TkDefaultFont", 11, "bold"),
            )

            canvas.create_text(
                width // 2,
                height // 2 + 15,
                text="Memory graph is currently empty",
                fill=self.TEXT_MUTED,
                font=("TkDefaultFont", 8),
            )

            return

        display_nodes = nodes[:80]
        node_positions = {}

        cx = width / 2
        cy = height / 2

        count = len(display_nodes)

        # Start with a stable circular layout, then relax it using
        # a lightweight force-directed simulation based on real edges.
        if count == 1:
            node_positions[display_nodes[0][0]] = (cx, cy)
        else:
            radius = min(width, height) * 0.30

            for index, (node_id, node) in enumerate(display_nodes):
                angle = 2.0 * math.pi * index / count

                node_positions[node_id] = (
                    cx + math.cos(angle) * radius,
                    cy + math.sin(angle) * radius,
                )

        display_ids = set(node_positions)

        graph_edges = [
            edge
            for edge in edges
            if (
                edge.get("source") in display_ids
                and edge.get("target") in display_ids
            )
        ]

        # Lightweight force-directed relaxation.
        # Stronger MemoryEdge weights attract connected memories more.
        for _ in range(80):
            forces = {
                node_id: [0.0, 0.0]
                for node_id in node_positions
            }

            positions = node_positions

            for source in display_ids:
                x1, y1 = positions[source]

                for target in display_ids:
                    if source >= target:
                        continue

                    x2, y2 = positions[target]

                    dx = x2 - x1
                    dy = y2 - y1
                    distance = max(
                        math.hypot(dx, dy),
                        1.0,
                    )

                    repulsion = 18000.0 / (distance * distance)

                    fx = dx / distance * repulsion
                    fy = dy / distance * repulsion

                    forces[source][0] -= fx
                    forces[source][1] -= fy
                    forces[target][0] += fx
                    forces[target][1] += fy

            for edge in graph_edges:
                source = edge["source"]
                target = edge["target"]
                weight = max(
                    0.1,
                    float(edge.get("weight", 1.0)),
                )

                x1, y1 = positions[source]
                x2, y2 = positions[target]

                dx = x2 - x1
                dy = y2 - y1
                distance = max(
                    math.hypot(dx, dy),
                    1.0,
                )

                desired = max(
                    70.0,
                    145.0 - min(weight, 10.0) * 7.0,
                )

                attraction = (
                    (distance - desired)
                    * 0.018
                    * min(weight, 4.0)
                )

                fx = dx / distance * attraction
                fy = dy / distance * attraction

                forces[source][0] += fx
                forces[source][1] += fy
                forces[target][0] -= fx
                forces[target][1] -= fy

            for node_id, (x, y) in positions.items():
                fx, fy = forces[node_id]

                node_positions[node_id] = (
                    min(
                        width - 45,
                        max(45, x + max(-8, min(8, fx))),
                    ),
                    min(
                        height - 45,
                        max(45, y + max(-8, min(8, fy))),
                    ),
                )

        self.node_positions = node_positions

        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            weight = edge.get("weight", 1.0)

            if (
                source not in node_positions
                or target not in node_positions
            ):
                continue

            x1, y1 = node_positions[source]
            x2, y2 = node_positions[target]

            line_width = max(
                1,
                min(5, int(round(weight))),
            )

            is_active = (source, target) in active_edges

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=self.YELLOW if is_active else self.BORDER_LIGHT,
                width=line_width + 2 if is_active else line_width,
            )

        if self.active_edges and self.node_positions:
            for source, target in self.active_edges:
                if (
                    source not in self.node_positions
                    or target not in self.node_positions
                ):
                    continue

                x1, y1 = self.node_positions[source]
                x2, y2 = self.node_positions[target]

                progress = self.pulse_progress

                pulse_x = x1 + (x2 - x1) * progress
                pulse_y = y1 + (y2 - y1) * progress

                canvas.create_oval(
                    pulse_x - 5,
                    pulse_y - 5,
                    pulse_x + 5,
                    pulse_y + 5,
                    fill=self.YELLOW,
                    outline=self.YELLOW,
                )

        for node_id, node in display_nodes:
            x, y = node_positions[node_id]

            memory_type = node.get("memory_type", "")
            activation_count = node.get("activation_count", 1)
            content = node.get("content", node_id)

            node_color = memory_type_color(memory_type)

            node_radius = 16 + min(
                12,
                max(0, activation_count - 1),
            )

            canvas.create_oval(
                x - node_radius,
                y - node_radius,
                x + node_radius,
                y + node_radius,
                fill=self.SURFACE_3,
                outline=node_color,
                width=2,
            )

            label = format_memory_content(
                content,
                20,
            )

            canvas.create_text(
                x,
                y,
                text=label,
                fill=self.TEXT,
                font=("TkDefaultFont", 7, "bold"),
                width=120,
            )

        canvas.create_text(
            10,
            10,
            text=(
                f"{len(nodes)} nodes  •  "
                f"{len(edges)} connections"
            ),
            anchor="nw",
            fill=self.TEXT_MUTED,
            font=("TkDefaultFont", 7),
        )

        if len(nodes) > len(display_nodes):
            canvas.create_text(
                width - 10,
                10,
                text=(
                    f"Showing {len(display_nodes)} "
                    f"of {len(nodes)} nodes"
                ),
                anchor="ne",
                fill=self.YELLOW,
                font=("TkDefaultFont", 7),
            )

    def _animate_pulse(self):
        if not self.graph_canvas or not self.active_edges:
            self.pulse_job = None
            return

        self.pulse_progress += 0.08

        if self.pulse_progress >= 1.0:
            self.pulse_progress = 0.0
            self.active_edges.clear()
            self.pulse_job = None
            self.draw_graph()
            return

        self.draw_graph()

        self.pulse_job = self.graph_canvas.after(
            30,
            self._animate_pulse,
        )

    def refresh(self, snapshot):
        memory_snapshot = snapshot.get("memory", {})
        graph_snapshot = snapshot.get("memory_graph", {})
        memory_activity = snapshot.get("memory_activity", {})

        nodes = graph_snapshot.get("nodes", {})
        edges = graph_snapshot.get("edges", {})

        self.memory_metrics["nodes"].configure(
            text=str(len(nodes))
        )

        self.memory_metrics["connections"].configure(
            text=str(len(edges))
        )

        episodic_count = sum(
            1
            for node in nodes.values()
            if str(node.get("memory_type", "")).upper() == "EPISODIC"
        )

        self.memory_metrics["experiences"].configure(
            text=str(episodic_count)
        )

        self.memory_metrics["last_update"].configure(
            text="—"
        )

        recent_items = list(memory_snapshot.get("episodic", [])[-3:])

        if not recent_items:
            self.recent_memory_label.configure(
                text="No recent memory data",
                fg=self.TEXT_SECONDARY,
            )
        else:
            lines = []

            for item in reversed(recent_items):
                lines.append(
                    "• "
                    + format_memory_content(
                        item,
                        70,
                    )
                )

            self.recent_memory_label.configure(
                text="\n".join(lines),
                fg=self.TEXT,
            )

        self.active_edges = {
            tuple(edge)
            for edge in memory_activity.get("edges", [])
        }

        if self.active_edges:
            self.pulse_progress = 0.0

            if self.pulse_job is None and self.graph_canvas is not None:
                self.pulse_job = self.graph_canvas.after(
                    30,
                    self._animate_pulse,
                )

        self.draw_graph(
            nodes,
            edges,
            memory_activity,
        )

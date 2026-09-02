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

    def draw_graph(self):
        canvas = self.graph_canvas

        if canvas is None:
            return

        canvas.delete("all")

        graph = self.runtime.memory.memory_graph

        nodes = list(graph.nodes.items())
        edges = list(graph.edges.values())

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
        radius = min(width, height) * 0.32
        count = len(display_nodes)

        if count == 1:
            node_positions[display_nodes[0][0]] = (cx, cy)
        else:
            for index, (node_id, node) in enumerate(display_nodes):
                angle = 2.0 * math.pi * index / count

                x = cx + math.cos(angle) * radius
                y = cy + math.sin(angle) * radius

                node_positions[node_id] = (x, y)

        for edge in edges:
            if (
                edge.source not in node_positions
                or edge.target not in node_positions
            ):
                continue

            x1, y1 = node_positions[edge.source]
            x2, y2 = node_positions[edge.target]

            line_width = max(
                1,
                min(5, int(round(edge.weight))),
            )

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=self.BORDER_LIGHT,
                width=line_width,
            )

        for node_id, node in display_nodes:
            x, y = node_positions[node_id]

            node_color = memory_type_color(node.memory_type)

            node_radius = 16 + min(
                12,
                max(0, node.activation_count - 1),
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
                node.content,
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
                f"{len(graph.nodes)} nodes  •  "
                f"{len(graph.edges)} connections"
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

    def refresh(self):
        memory = self.runtime.memory
        state = memory.snapshot()
        graph = memory.memory_graph

        self.memory_metrics["nodes"].configure(
            text=str(len(graph.nodes))
        )

        self.memory_metrics["connections"].configure(
            text=str(len(graph.edges))
        )

        episodic_count = sum(
            1
            for node in graph.nodes.values()
            if str(node.memory_type).upper() == "EPISODIC"
        )

        self.memory_metrics["experiences"].configure(
            text=str(episodic_count)
        )

        self.memory_metrics["last_update"].configure(
            text="—"
        )

        recent_items = list(state.episodic[-3:])

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

        self.draw_graph()

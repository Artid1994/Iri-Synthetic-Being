import unittest
from unittest.mock import MagicMock

from ui.memory_panel import MemoryPanel


class TestMemoryPanelActivationTelemetry(unittest.TestCase):
    def setUp(self):
        self.parent = MagicMock()
        self.runtime = MagicMock()
        self.panel_builder = MagicMock()
        self.panel_header_builder = MagicMock()
        self.colors = {
            "SURFACE": "#1e1e1e",
            "SURFACE_2": "#252526",
            "SURFACE_3": "#2d2d30",
            "BORDER": "#3e3e42",
            "CYAN": "#00ffff",
            "YELLOW": "#ffff00",
            "TEXT": "#ffffff",
            "TEXT_MUTED": "#888888",
        }
        self.panel = MemoryPanel(
            self.parent,
            self.runtime,
            self.panel_builder,
            self.panel_header_builder,
            self.colors,
        )
        self.mock_canvas = MagicMock()
        self.mock_canvas.winfo_width.return_value = 500
        self.mock_canvas.winfo_height.return_value = 500
        self.panel.graph_canvas = self.mock_canvas

    def test_active_memory_node_illuminates_from_telemetry(self):
        nodes = {
            "node_1": {"content": "Episodic Memory Alpha", "memory_type": "episodic", "activation_count": 1},
            "node_2": {"content": "Semantic Fact Beta", "memory_type": "semantic", "activation_count": 1},
        }
        edges = {}
        activity = {"nodes": ["node_1"]}

        self.panel.draw_graph(nodes=nodes, edges=edges, activity=activity)

        # Check oval creations on canvas
        oval_calls = self.mock_canvas.create_oval.call_args_list
        self.assertEqual(len(oval_calls), 2)

        # First call is node_1 (active): should use CYAN fill and YELLOW outline
        call_active = oval_calls[0]
        self.assertEqual(call_active.kwargs.get("fill"), "#00ffff")
        self.assertEqual(call_active.kwargs.get("outline"), "#ffff00")
        self.assertEqual(call_active.kwargs.get("width"), 3)

        # Second call is node_2 (inactive): should use SURFACE_3 fill
        call_inactive = oval_calls[1]
        self.assertEqual(call_inactive.kwargs.get("fill"), "#2d2d30")
        self.assertEqual(call_inactive.kwargs.get("width"), 2)


if __name__ == "__main__":
    unittest.main()

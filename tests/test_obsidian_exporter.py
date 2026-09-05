import json
import shutil
import tempfile
import unittest
from pathlib import Path

from runtime.memory_graph import MemoryGraph
from runtime.obsidian_exporter import ObsidianMemoryExporter, MANIFEST_FILENAME, sanitize_filename


class TestObsidianMemoryExporter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.export_path = Path(self.temp_dir) / "ae01m_memory"
        self.exporter = ObsidianMemoryExporter(self.export_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename("Simple Text"), "Simple_Text")
        self.assertEqual(sanitize_filename("Path/Traversal/../Danger:!"), "Path_Traversal_Danger")
        self.assertEqual(sanitize_filename("   "), "item")
        self.assertEqual(sanitize_filename("Special@#$%^&*()_+"), "Special")

    def test_basic_node_export_and_frontmatter(self):
        graph = MemoryGraph()
        graph.add_node("Python Programming", "EPISODIC")

        stats = self.exporter.export(graph)
        self.assertEqual(stats["exported"], 1)
        self.assertEqual(stats["cleaned"], 0)

        expected_file = self.export_path / "EPISODIC__Python_Programming.md"
        self.assertTrue(expected_file.is_file())

        content = expected_file.read_text(encoding="utf-8")
        self.assertIn('id: "EPISODIC:Python Programming"', content)
        self.assertIn('type: "EPISODIC"', content)
        self.assertIn("activation_count: 1", content)
        self.assertIn("# Python Programming", content)

    def test_directed_edge_to_wikilink_and_resolution(self):
        graph = MemoryGraph()
        n1 = graph.add_node("Python", "EPISODIC")
        n2 = graph.add_node("Language", "SEMANTIC")
        graph.connect(n1, n2)

        self.exporter.export(graph)

        source_file = self.export_path / "EPISODIC__Python.md"
        target_file = self.export_path / "SEMANTIC__Language.md"
        self.assertTrue(source_file.is_file())
        self.assertTrue(target_file.is_file())

        source_content = source_file.read_text(encoding="utf-8")
        # Wikilink to target stem without .md extension
        self.assertIn("[[SEMANTIC__Language|Language]]", source_content)
        self.assertIn("weight: 1.00", source_content)

    def test_sanitization_collision_handling(self):
        graph = MemoryGraph()
        # Two different raw contents that sanitize to the same base stem
        graph.add_node("Topic & One", "EPISODIC")
        graph.add_node("Topic / One", "EPISODIC")

        stats = self.exporter.export(graph)
        self.assertEqual(stats["exported"], 2)

        files = list(self.export_path.glob("*.md"))
        self.assertEqual(len(files), 2)
        # Ensure distinct filenames
        filenames = [f.name for f in files]
        self.assertEqual(len(set(filenames)), 2)

    def test_deterministic_repeated_export(self):
        graph = MemoryGraph()
        n1 = graph.add_node("Node A", "EPISODIC")
        n2 = graph.add_node("Node B", "SEMANTIC")
        graph.connect(n1, n2)

        # First export
        stats1 = self.exporter.export(graph)
        manifest_path = self.export_path / MANIFEST_FILENAME
        manifest_data1 = manifest_path.read_text(encoding="utf-8")

        # Second export of identical graph
        stats2 = self.exporter.export(graph)
        manifest_data2 = manifest_path.read_text(encoding="utf-8")

        self.assertEqual(stats1["exported"], stats2["exported"])
        self.assertEqual(stats2["cleaned"], 0)
        self.assertEqual(manifest_data1, manifest_data2)

    def test_manifest_creation_and_pruned_node_cleanup(self):
        graph = MemoryGraph()
        n1 = graph.add_node("Node to Keep", "EPISODIC")
        n2 = graph.add_node("Node to Remove", "EPISODIC")

        self.exporter.export(graph)
        file_to_remove = self.export_path / "EPISODIC__Node_to_Remove.md"
        self.assertTrue(file_to_remove.is_file())

        # Simulate graph change: remove node from graph dictionary
        del graph.nodes[n2]

        stats = self.exporter.export(graph)
        self.assertEqual(stats["exported"], 1)
        self.assertEqual(stats["cleaned"], 1)
        self.assertFalse(file_to_remove.exists())

        # Verify manifest reflects update
        manifest = json.loads((self.export_path / MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertIn(n1, manifest["managed_files"])
        self.assertNotIn(n2, manifest["managed_files"])

    def test_does_not_delete_unmanaged_user_files(self):
        graph = MemoryGraph()
        graph.add_node("Node A", "EPISODIC")
        self.exporter.export(graph)

        # Create a user file not in manifest
        user_file = self.export_path / "user_notes.md"
        user_file.write_text("User created note", encoding="utf-8")

        # Re-export graph
        self.exporter.export(graph)
        # User file must remain untouched
        self.assertTrue(user_file.is_file())
        self.assertEqual(user_file.read_text(encoding="utf-8"), "User created note")


if __name__ == "__main__":
    unittest.main()

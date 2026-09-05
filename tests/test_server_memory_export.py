import shutil
import tempfile
import unittest
from pathlib import Path
from starlette.testclient import TestClient

import server


class TestServerMemoryExportAPI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.orig_export_dir = server.VAULT_EXPORT_DIR
        server.VAULT_EXPORT_DIR = Path(self.temp_dir) / "vault_memory"
        self.client = TestClient(server.app)

    def tearDown(self):
        server.VAULT_EXPORT_DIR = self.orig_export_dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_export_endpoint_exists_and_returns_success(self):
        # Ingest a memory into the live runtime_engine
        server.runtime_engine.memory.add_experience("FastAPI Backend")
        server.runtime_engine.memory.associate("FastAPI Backend", "Server")

        response = self.client.post("/api/memory/export")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("exported", data)
        self.assertIn("cleaned", data)
        self.assertGreaterEqual(data["exported"], 2)
        self.assertEqual(data["destination"], "vault_memory")

        # Verify physical files written to the server's configured destination
        exported_files = [f.name for f in server.VAULT_EXPORT_DIR.glob("*.md")]
        self.assertTrue(any("FastAPI_Backend" in name for name in exported_files))
        self.assertTrue(any("Server" in name for name in exported_files))

    def test_arbitrary_client_payload_is_ignored(self):
        # Attempt path traversal or arbitrary path injection via payload
        payload = {"destination": "/etc/passwd", "path": "../../danger"}
        response = self.client.post("/api/memory/export", json=payload)
        self.assertEqual(response.status_code, 200)

        # Destination must strictly remain the configured server directory
        self.assertEqual(response.json()["destination"], "vault_memory")
        self.assertFalse(Path("/etc/passwd.md").exists())

    def test_export_failure_returns_500_without_leaking_stacktrace(self):
        # Simulate an export directory that cannot be created/written to (e.g. invalid path)
        class FaultyExporter:
            def __init__(self, _):
                pass

            def export(self, _):
                raise RuntimeError("Disk simulation error with private stack details")

        orig_class = server.ObsidianMemoryExporter
        server.ObsidianMemoryExporter = FaultyExporter
        try:
            response = self.client.post("/api/memory/export")
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Memory export operation failed"})
            # Verify stack trace is not exposed
            self.assertNotIn("Disk simulation error", response.text)
        finally:
            server.ObsidianMemoryExporter = orig_class


if __name__ == "__main__":
    unittest.main()

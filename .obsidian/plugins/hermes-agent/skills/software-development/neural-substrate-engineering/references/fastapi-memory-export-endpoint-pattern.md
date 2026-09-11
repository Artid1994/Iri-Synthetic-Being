# FastAPIMemoryExportEndpointPattern

## Context
When connecting external workspace tools (such as Obsidian via Community Plugins) to a local cognitive runtime, a secure, unidirectional export API is required.

## Key Principles & Guardrails
1. **Unidirectional Projection Only**: The endpoint triggers an export from in-memory runtime data structures (`MemoryGraph`) to an isolated filesystem directory (`vault_memory`). It does NOT read filesystem edits back into the cognitive runtime.
2. **Strict Server-Controlled Path Boundary**:
   - Never accept an export destination path from client HTTP request bodies or query parameters.
   - Lock `VAULT_EXPORT_DIR` to a resolved server-side constant within project boundaries.
   - Ignore or reject arbitrary client-supplied path overrides to prevent path traversal.
3. **No Internal Stack Trace Leaks**: Catch exporter exceptions and raise generic HTTP 500 (`"Memory export operation failed"`) without exposing disk structure or runtime traces to clients.
4. **Zero Impact on Core Models**: The endpoint consumes public attributes (`runtime_engine.memory.memory_graph`) through an external exporter (`ObsidianMemoryExporter`) without modifying `MemoryGraph`, `Memory`, `Brain`, or cognitive loop architecture.
5. **Deterministic Statistics in Response**: Return count summaries (`exported`, `cleaned`, `destination`) for client feedback and status bar reporting.

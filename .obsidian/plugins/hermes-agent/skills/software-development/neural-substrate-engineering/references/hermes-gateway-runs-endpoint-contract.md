# Hermes Gateway Architecture & Endpoint Mapping

When integrating client extensions (such as the Obsidian `hermes-agent` community plugin) with local Hermes infrastructure:

## 1. Process Separation: `hermes serve` vs `hermes gateway`

Do not conflate the two separate Hermes background services:

### `hermes serve`
- **Purpose**: Web UI / Dashboard / Desktop application backend (FastAPI / Uvicorn).
- **Default Port**: `9119` (configurable via `--port`).
- **Endpoints**:
  * `/api/models`, `/api/sessions`, `/api/cron`, `/api/skills`, `/api/tools`, `/api/ws`, `/api/pty`.
- **Key Invariant**: Does **NOT** provide agent run management routes such as `/v1/runs`. Sending `POST /v1/runs` will return a 404 error from the headless web backend.

### `hermes gateway run` (with `api_server` platform enabled)
- **Purpose**: OpenAI-compatible REST API server and persistent agent run management (`gateway/platforms/api_server.py`).
- **Default Port**: `8642` (`DEFAULT_PORT = 8642`).
- **Endpoints**:
  * `POST /v1/runs` — start an agent run, returns `run_id` immediately (202).
  * `GET /v1/runs/{run_id}` — poll run status.
  * `GET /v1/runs/{run_id}/events` — SSE stream of structured lifecycle events (`tool.started`, `tool.completed`, `run.completed`, etc.).
  * `POST /v1/runs/{run_id}/approval` — resolve a pending run approval.
  * `POST /v1/runs/{run_id}/steer` — inject mid-run guidance.
  * `POST /v1/runs/{run_id}/stop` — interrupt a running agent.
  * `GET /health` — health check.

## 2. Authentication Contract
- Client plugins configured with an API key send:
  ```http
  Authorization: Bearer <API_SERVER_KEY>
  ```
- The `api_server` verifies the bearer token against `API_SERVER_KEY` (configured via env var or `platforms.api_server.extra.key`).
- Requests without a valid Bearer token are rejected with `HTTP 401 Unauthorized`.

## 3. Launching the Compatible Endpoint
To support clients calling `POST /v1/runs` on port 8642:
```bash
API_SERVER_KEY="<token>" /home/artid1994/.local/bin/hermes gateway run
```
Never attempt to reconfigure `hermes serve` to handle `/v1/runs`, as it belongs strictly to the gateway's `api_server` adapter.

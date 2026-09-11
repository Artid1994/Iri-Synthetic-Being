# Hermes Gateway Port Configuration & Startup Verification

When testing or integrating external clients (e.g. Obsidian community plugins, remote GUIs, mobile connectors) that communicate with the local Hermes Agent Gateway:

## 1. Gateway Port Discrepancies
- Default CLI headless server port: `hermes serve` binds to port `9119` by default.
- External community plugins or clients may have hard-coded or default endpoints expecting a different port (e.g. `http://127.0.0.1:8642`).
- Never edit client source code or plugin files to fix a port mismatch when the CLI itself provides a documented port configuration option.

## 2. Documented Port Option
Inspect `hermes serve --help` to confirm options:
- `--port PORT`: Specify custom bind port (e.g. `--port 8642`).
- `--host HOST`: Host bind interface (default `127.0.0.1`).
- `--skip-build`: Skips web frontend asset compilation (essential for headless/daemon runs without node/npm build dependencies).

Command pattern:
```bash
/path/to/hermes serve --port <PORT> --skip-build
```

## 3. Port Listening & Health Verification
1. Verify listener:
   ```bash
   ss -tulpn | grep <PORT>
   ```
2. Endpoint probes:
   - Root (`/`): Returns JSON explaining headless mode:
     `{"error":"Headless backend (hermes serve): web UI disabled — use hermes dashboard for the browser UI."}`
   - API runs (`/v1/runs`): Returns HTTP 401 (`{"detail":"Unauthorized"}`) when unauthenticated, confirming endpoint existence and active security gateway without false positive 404s.

## 4. Lifecycle Cleanliness
Always terminate background test gateway processes (`kill <PID>`) after verification to avoid port exhaustion or ghost listeners on the development machine.

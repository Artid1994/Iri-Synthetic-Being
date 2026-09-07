# Obsidian Minimal Connector Plugin Pattern (O5B / O5C)

When implementing an Obsidian Community Plugin to act as an external viewer/control surface for an independent local backend (e.g. AE01M):

## Architectural Boundaries
1. **External View Only**: The host engine (Python/FastAPI) remains the single authoritative source of truth. The Obsidian plugin never owns or mutates core runtime data structures directly.
2. **One-Way Projection**:
   ```text
   Obsidian Plugin → HTTP POST → Server Gateway → Engine MemoryGraph → Markdown Exporter → Vault Projection Folder
   ```
   Never read generated Markdown files back into the engine memory graph.
3. **No Bundling / Forking**: Do not bundle the Obsidian binary, do not fork Obsidian source code, and do not modify core `.obsidian/*.json` configurations without explicit approval.

## Minimal Community Plugin Anatomy
Obsidian community plugins live in `.obsidian/plugins/<plugin-id>/`:
- `manifest.json`:
  ```json
  {
    "id": "ae01m-connector",
    "name": "AE01M Connector",
    "version": "0.1.0",
    "minAppVersion": "1.0.0",
    "description": "Connects Obsidian workspace to the local backend gateway.",
    "author": "AE01M Project",
    "isDesktopOnly": true
  }
  ```
- `main.js`: Compact CommonJS file using `obsidian` module APIs:
  ```javascript
  "use strict";
  const { Plugin, Notice, requestUrl, PluginSettingTab, Setting } = require("obsidian");

  const DEFAULT_SETTINGS = { serverUrl: "http://localhost:3001" };

  class AE01MConnectorPlugin extends Plugin {
      async onload() {
          await this.loadSettings();

          // Status bar indicator
          this.statusBarItem = this.addStatusBarItem();
          this.updateStatusBar("Ready");

          // Command registration
          this.addCommand({
              id: "ae01m-sync-memory",
              name: "AE01M: Sync Memory to Vault",
              callback: async () => { await this.triggerMemorySync(); }
          });

          // Minimal settings tab
          this.addSettingTab(new AE01MSettingTab(this.app, this));
      }

      updateStatusBar(status) {
          if (this.statusBarItem) this.statusBarItem.setText(`AE01M: ${status}`);
      }

      async triggerMemorySync() {
          this.updateStatusBar("Syncing");
          const endpoint = `${this.settings.serverUrl.replace(/\/+$/, "")}/api/memory/export`;
          try {
              const response = await requestUrl({
                  url: endpoint,
                  method: "POST",
                  headers: { "Content-Type": "application/json" }
              });

              if (response.status === 200) {
                  const data = response.json;
                  this.updateStatusBar("Synced");
                  new Notice(`AE01M: Memory synced (${data.exported || 0} exported, ${data.cleaned || 0} cleaned)`);
              } else {
                  this.updateStatusBar("Error");
                  new Notice("AE01M: Memory sync failed with server error");
              }
          } catch (err) {
              this.updateStatusBar("Error");
              new Notice("AE01M: Unable to connect to local AE01M server");
          }
      }

      async loadSettings() { this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData()); }
      async saveSettings() { await this.saveData(this.settings); }
  }

  class AE01MSettingTab extends PluginSettingTab {
      constructor(app, plugin) { super(app, plugin); this.plugin = plugin; }
      display() {
          const { containerEl } = this;
          containerEl.empty();
          containerEl.createEl("h2", { text: "AE01M Connector Settings" });
          new Setting(containerEl)
              .setName("Server URL")
              .setDesc("The address of the local AE01M Gateway")
              .addText((text) => text
                  .setPlaceholder("http://localhost:3001")
                  .setValue(this.plugin.settings.serverUrl)
                  .onChange(async (val) => {
                      this.plugin.settings.serverUrl = val.trim() || DEFAULT_SETTINGS.serverUrl;
                      await this.plugin.saveSettings();
                  }));
      }
  }

  module.exports = AE01MConnectorPlugin;
  ```

## Verification & Headless Pitfalls
1. **Node syntax check**: Run `node -c .obsidian/plugins/<id>/main.js` to ensure zero syntax or export errors.
2. **HTTP communication**: `requestUrl` avoids Electron/CORS issues for local HTTP communication.
3. **Headless vs GUI distinction**: In a headless or terminal-only environment, distinguish:
   - `VERIFIED (VIA BACKEND HTTP)`: Endpoint responds correctly with JSON.
   - `STRUCTURALLY VERIFIED`: Plugin JS syntax, manifest, and exports are validated.
   - `NOT VERIFIED IN LIVE GUI`: If no interactive Obsidian GUI session is running to observe physical Notice popups, status bar text, and Native Graph View node rendering, mark them explicitly as NOT VERIFIED rather than simulating.

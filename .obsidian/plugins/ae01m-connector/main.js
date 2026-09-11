"use strict";

const { Plugin, Notice, requestUrl, PluginSettingTab, Setting } = require("obsidian");

const DEFAULT_SETTINGS = {
    serverUrl: "http://localhost:3001"
};

class AE01MConnectorPlugin extends Plugin {
    async onload() {
        await this.loadSettings();

        // 1. Status Bar Item
        this.statusBarItem = this.addStatusBarItem();
        this.updateStatusBar("Ready");

        // 2. Register Manual Memory Sync Command
        this.addCommand({
            id: "ae01m-sync-memory",
            name: "AE01M: Sync Memory to Vault",
            callback: async () => {
                await this.triggerMemorySync();
            }
        });

        // 3. Settings Tab
        this.addSettingTab(new AE01MSettingTab(this.app, this));
    }

    onunload() {
        // Obsidian automatically cleans up status bar and commands registered via this.add*
    }

    updateStatusBar(status) {
        if (this.statusBarItem) {
            this.statusBarItem.setText(`AE01M: ${status}`);
        }
    }

    async triggerMemorySync() {
        this.updateStatusBar("Syncing");
        const endpoint = `${this.settings.serverUrl.replace(/\/+$/, "")}/api/memory/export`;

        try {
            const response = await requestUrl({
                url: endpoint,
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            });

            if (response.status === 200) {
                const data = response.json;
                const exported = data.exported || 0;
                const cleaned = data.cleaned || 0;
                this.updateStatusBar("Synced");
                new Notice(`AE01M: Memory synced (${exported} exported, ${cleaned} cleaned)`);
            } else {
                this.updateStatusBar("Error");
                new Notice("AE01M: Memory sync failed with server error");
            }
        } catch (err) {
            this.updateStatusBar("Error");
            new Notice("AE01M: Unable to connect to local AE01M server");
        }
    }

    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }
}

class AE01MSettingTab extends PluginSettingTab {
    constructor(app, plugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display() {
        const { containerEl } = this;
        containerEl.empty();

        containerEl.createEl("h2", { text: "AE01M Connector Settings" });

        new Setting(containerEl)
            .setName("Server URL")
            .setDesc("The address of the local AE01M Cyber Human Brain Gateway")
            .addText((text) =>
                text
                    .setPlaceholder("http://localhost:3001")
                    .setValue(this.plugin.settings.serverUrl)
                    .onChange(async (value) => {
                        this.plugin.settings.serverUrl = value.trim() || DEFAULT_SETTINGS.serverUrl;
                        await this.plugin.saveSettings();
                    })
            );
    }
}

module.exports = AE01MConnectorPlugin;

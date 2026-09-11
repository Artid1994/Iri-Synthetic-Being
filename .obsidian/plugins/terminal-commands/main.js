'use strict';

var node_child_process = require('node:child_process');
var node_path = require('node:path');
var obsidian = require('obsidian');
var node_fs = require('node:fs');
var node_os = require('node:os');
var electron = require('electron');

const truncateTerminalName = (value) => {
    const characters = [...value];
    return characters.length > 8
        ? `${characters.slice(0, 8).join('')}…`
        : value;
};
const CURRENT_SETTINGS_VERSION = 3;
const INITIAL_TERMINAL_ID = 'terminal-1';
const WINDOWS_POWERSHELL_TERMINAL_ID = 'terminal-powershell';
const DEFAULT_COMMANDS = [
    {
        id: 'open-terminal',
        kind: 'open-terminal',
        name: 'Open in terminal',
        command: '',
        workingDirectory: 'vault',
        keepTerminalOpen: true
    },
    {
        id: 'claude',
        kind: 'shell-command',
        name: 'Open in Claude Code',
        command: 'claude',
        workingDirectory: 'vault',
        keepTerminalOpen: true
    },
    {
        id: 'codex',
        kind: 'shell-command',
        name: 'Open in Codex cli',
        command: 'codex',
        workingDirectory: 'vault',
        keepTerminalOpen: true
    },
    {
        id: 'antigravity',
        kind: 'shell-command',
        name: 'Open in Antigravity',
        command: 'agy --dangerously-skip-permissions',
        workingDirectory: 'vault',
        keepTerminalOpen: true
    },
    {
        id: 'opencode',
        kind: 'shell-command',
        name: 'Open in OpenCode',
        command: 'opencode',
        workingDirectory: 'vault',
        keepTerminalOpen: true
    },
    {
        id: 'git-pull',
        kind: 'shell-command',
        name: 'Git: pull',
        command: 'git pull',
        workingDirectory: 'vault',
        keepTerminalOpen: true
    },
    {
        id: 'vscode',
        kind: 'shell-command',
        name: 'Open in VS Code',
        command: 'code .',
        workingDirectory: 'vault',
        keepTerminalOpen: false
    }
];
const WINDOWS_DEFAULT_COMMANDS = [
    {
        id: 'file-explorer',
        kind: 'shell-command',
        name: 'Open in File Explorer',
        command: 'explorer .',
        workingDirectory: 'vault',
        keepTerminalOpen: false
    }
];
const defaultTerminalName = () => {
    if (!obsidian.Platform.isDesktopApp) {
        return '';
    }
    if (obsidian.Platform.isMacOS) {
        return 'Terminal';
    }
    if (obsidian.Platform.isWin) {
        return 'cmd';
    }
    if (obsidian.Platform.isLinux) {
        return 'x-terminal-emulator';
    }
    return '';
};
const resolveExecutableFromPath = (value) => {
    const executable = value.trim().replace(/^"(.*)"$/, '$1');
    if (!executable) {
        return '';
    }
    const isExecutableAbsolute = obsidian.Platform.isWin
        ? node_path.win32.isAbsolute(executable)
        : node_path.isAbsolute(executable);
    if (isExecutableAbsolute) {
        return executable;
    }
    const extensions = obsidian.Platform.isWin && !node_path.win32.extname(executable)
        ? ['', '.exe']
        : [''];
    for (const directory of (process.env.PATH ?? '').split(node_path.delimiter)) {
        if (!directory) {
            continue;
        }
        for (const extension of extensions) {
            const candidate = node_path.join(directory, `${executable}${extension}`);
            if (node_fs.existsSync(candidate)) {
                return candidate;
            }
        }
    }
    return executable;
};
const defaultWindowsCmdApp = () => {
    const windowsRoot = process.env.SystemRoot ?? process.env.WINDIR;
    if (windowsRoot) {
        const systemCmd = node_path.win32.join(windowsRoot, 'System32', 'cmd.exe');
        if (node_fs.existsSync(systemCmd)) {
            return systemCmd;
        }
    }
    return resolveExecutableFromPath(process.env.ComSpec ?? 'cmd.exe');
};
const normalizeExecutablePath = (value) => {
    const resolved = resolveExecutableFromPath(value);
    if (!obsidian.Platform.isWin || node_path.win32.basename(resolved).toLowerCase() !== 'cmd.exe') {
        return resolved;
    }
    const defaultCmd = defaultWindowsCmdApp();
    return node_path.win32.normalize(resolved).toLowerCase() ===
        node_path.win32.normalize(defaultCmd).toLowerCase()
        ? defaultCmd
        : resolved;
};
const defaultTerminalApp = () => {
    if (!obsidian.Platform.isDesktopApp) {
        return '';
    }
    if (obsidian.Platform.isWin) {
        return defaultWindowsCmdApp();
    }
    if (obsidian.Platform.isMacOS) {
        const terminalApp = '/System/Applications/Utilities/Terminal.app';
        return node_fs.existsSync(terminalApp) ? terminalApp : 'Terminal';
    }
    if (obsidian.Platform.isLinux) {
        return resolveExecutableFromPath('x-terminal-emulator');
    }
    return '';
};
const getCurrentDesktopPlatform = () => {
    if (!obsidian.Platform.isDesktopApp) {
        return null;
    }
    if (obsidian.Platform.isMacOS) {
        return 'macos';
    }
    if (obsidian.Platform.isWin) {
        return 'win';
    }
    if (obsidian.Platform.isLinux) {
        return 'linux';
    }
    return null;
};
const buildDefaultTerminalAppSetting = () => {
    const platform = getCurrentDesktopPlatform();
    const app = defaultTerminalApp();
    if (!platform) {
        return {};
    }
    return { [platform]: app };
};
const buildDefaultTerminalProfile = (applications = buildDefaultTerminalAppSetting()) => ({
    id: INITIAL_TERMINAL_ID,
    name: defaultTerminalName(),
    applications
});
const defaultWindowsPowerShellApp = () => {
    const windowsRoot = process.env.SystemRoot ?? process.env.WINDIR;
    if (windowsRoot) {
        const systemPowerShell = node_path.win32.join(windowsRoot, 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe');
        if (node_fs.existsSync(systemPowerShell)) {
            return systemPowerShell;
        }
    }
    return resolveExecutableFromPath('powershell.exe');
};
const buildDefaultWindowsPowerShellProfile = () => ({
    id: WINDOWS_POWERSHELL_TERMINAL_ID,
    name: 'powershell',
    applications: { win: defaultWindowsPowerShellApp() }
});
const createDefaultTerminalProfiles = () => obsidian.Platform.isWin
    ? [buildDefaultTerminalProfile(), buildDefaultWindowsPowerShellProfile()]
    : [buildDefaultTerminalProfile()];
const cloneDefaultCommands = () => {
    const commands = obsidian.Platform.isWin
        ? [...DEFAULT_COMMANDS, ...WINDOWS_DEFAULT_COMMANDS]
        : DEFAULT_COMMANDS;
    return commands.map((command) => ({
        ...command,
        terminalId: INITIAL_TERMINAL_ID
    }));
};
const DEFAULT_SETTINGS = {
    settingsVersion: CURRENT_SETTINGS_VERSION,
    terminals: createDefaultTerminalProfiles(),
    reuseExistingMacApp: true,
    commands: cloneDefaultCommands()
};
const isRecord = (value) => typeof value === 'object' && value !== null;
const normalizeTerminalAppSetting = (value, fallback) => {
    const platform = getCurrentDesktopPlatform();
    if (isRecord(value)) {
        const next = {};
        if (typeof value.win === 'string') {
            next.win = value.win.trim();
        }
        if (typeof value.macos === 'string') {
            next.macos = value.macos.trim();
        }
        if (typeof value.linux === 'string') {
            next.linux = value.linux.trim();
        }
        if (platform && next[platform]) {
            next[platform] = normalizeExecutablePath(next[platform]);
        }
        return next;
    }
    if (!platform) {
        return { ...fallback };
    }
    return {
        [platform]: normalizeExecutablePath(fallback[platform] ?? '')
    };
};
const readBoolean = (value, fallback) => typeof value === 'boolean' ? value : fallback;
const normalizeWorkingDirectory = (value) => value === 'current-note' ? 'current-note' : 'vault';
const normalizeId = (value) => {
    if (typeof value !== 'string') {
        return null;
    }
    const normalized = value.trim().toLowerCase();
    return /^[a-z0-9][a-z0-9-]*$/.test(normalized) ? normalized : null;
};
const createUniqueId = (usedIds, prefix) => {
    let id;
    do {
        id = `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
    } while (usedIds.has(id));
    return id;
};
const normalizeTerminalProfiles = (value, legacyTerminalApp) => {
    if (!Array.isArray(value)) {
        return [
            buildDefaultTerminalProfile(normalizeTerminalAppSetting(legacyTerminalApp, buildDefaultTerminalAppSetting()))
        ];
    }
    const usedIds = new Set();
    const terminals = [];
    for (const item of value) {
        if (!isRecord(item)) {
            continue;
        }
        let id = normalizeId(item.id);
        if (!id || usedIds.has(id)) {
            id = createUniqueId(usedIds, 'terminal');
        }
        usedIds.add(id);
        terminals.push({
            id,
            name: typeof item.name === 'string' ? item.name : '',
            applications: normalizeTerminalAppSetting(item.applications, buildDefaultTerminalAppSetting())
        });
    }
    return terminals.length > 0 ? terminals : createDefaultTerminalProfiles();
};
const normalizeCommands = (value, terminalIds, fallbackTerminalId) => {
    if (!Array.isArray(value)) {
        return cloneDefaultCommands().map((command) => ({
            ...command,
            terminalId: fallbackTerminalId
        }));
    }
    const usedIds = new Set();
    const commands = [];
    for (const item of value) {
        if (!isRecord(item)) {
            continue;
        }
        let id = normalizeId(item.id);
        if (!id || usedIds.has(id)) {
            id = createUniqueId(usedIds, 'command');
        }
        usedIds.add(id);
        const terminalId = normalizeId(item.terminalId);
        const kind = item.kind === 'open-terminal' ? 'open-terminal' : 'shell-command';
        commands.push({
            id,
            kind,
            name: typeof item.name === 'string' ? item.name : '',
            command: kind === 'open-terminal'
                ? ''
                : typeof item.command === 'string'
                    ? item.command
                    : '',
            workingDirectory: normalizeWorkingDirectory(item.workingDirectory),
            keepTerminalOpen: kind === 'open-terminal'
                ? true
                : readBoolean(item.keepTerminalOpen, true),
            terminalId: terminalId && terminalIds.has(terminalId)
                ? terminalId
                : fallbackTerminalId
        });
    }
    return commands;
};
const createCommand = (existing, terminalId) => {
    const usedIds = new Set(existing.map((command) => command.id));
    return {
        id: createUniqueId(usedIds, 'command'),
        kind: 'shell-command',
        name: '',
        command: '',
        workingDirectory: 'vault',
        keepTerminalOpen: true,
        terminalId
    };
};
const createTerminalProfile = (existing) => {
    const usedIds = new Set(existing.map((terminal) => terminal.id));
    return {
        id: createUniqueId(usedIds, 'terminal'),
        name: '',
        applications: {}
    };
};
const addMigratedOpenTerminalCommand = (commands, terminalId) => {
    if (commands.some((command) => command.kind === 'open-terminal')) {
        return;
    }
    const usedIds = new Set(commands.map((command) => command.id));
    const id = usedIds.has('open-terminal')
        ? createUniqueId(usedIds, 'open-terminal')
        : 'open-terminal';
    commands.unshift({
        id,
        kind: 'open-terminal',
        name: 'Open in terminal',
        command: '',
        workingDirectory: 'vault',
        keepTerminalOpen: true,
        terminalId
    });
};
const addMigratedWindowsPowerShellTerminal = (terminals) => {
    if (!obsidian.Platform.isWin) {
        return;
    }
    const hasWindowsPowerShell = terminals.some((terminal) => {
        const executableName = node_path.win32.basename(terminal.applications.win ?? '').toLowerCase();
        return executableName === 'powershell' || executableName === 'powershell.exe';
    });
    if (hasWindowsPowerShell) {
        return;
    }
    const profile = buildDefaultWindowsPowerShellProfile();
    const usedIds = new Set(terminals.map((terminal) => terminal.id));
    if (usedIds.has(profile.id)) {
        profile.id = createUniqueId(usedIds, 'terminal-powershell');
    }
    terminals.push(profile);
};
const normalizeSettings = (stored) => {
    const source = isRecord(stored) ? stored : {};
    const terminals = normalizeTerminalProfiles(source.terminals, source.terminalApp);
    const fallbackTerminalId = terminals[0]?.id ?? INITIAL_TERMINAL_ID;
    const commands = normalizeCommands(source.commands, new Set(terminals.map((terminal) => terminal.id)), fallbackTerminalId);
    const storedVersion = typeof source.settingsVersion === 'number' ? source.settingsVersion : 0;
    if (storedVersion < 1) {
        addMigratedOpenTerminalCommand(commands, fallbackTerminalId);
    }
    if (storedVersion < 2) {
        addMigratedWindowsPowerShellTerminal(terminals);
    }
    return {
        settingsVersion: CURRENT_SETTINGS_VERSION,
        terminals,
        reuseExistingMacApp: readBoolean(source.reuseExistingMacApp, DEFAULT_SETTINGS.reuseExistingMacApp),
        commands
    };
};
const restoreDefaultTerminalProfiles = (settings) => {
    const defaultTerminals = createDefaultTerminalProfiles();
    const defaultTerminalIds = new Set(defaultTerminals.map((terminal) => terminal.id));
    const fallbackTerminalId = defaultTerminals[0]?.id ?? '';
    settings.terminals = defaultTerminals;
    for (const command of settings.commands) {
        if (!defaultTerminalIds.has(command.terminalId)) {
            command.terminalId = fallbackTerminalId;
        }
    }
};
const resolveTerminalProfile = (settings, terminalId) => settings.terminals.find((terminal) => terminal.id === terminalId) ??
    settings.terminals[0];
const getCurrentTerminalApp = (terminalApp) => {
    const platform = getCurrentDesktopPlatform();
    if (!platform) {
        return '';
    }
    return terminalApp[platform] ?? '';
};
const setCurrentTerminalApp = (terminalApp, value) => {
    const platform = getCurrentDesktopPlatform();
    if (!platform) {
        return { ...terminalApp };
    }
    return {
        ...terminalApp,
        [platform]: value.trim()
    };
};

const getLaunchTargetDirectoryLabel = (target) => target.workingDirectory === 'current-note' ? 'Note folder' : 'Vault folder';
const getLaunchTargetTerminalLabel = (target) => target.keepTerminalOpen ? 'Keep terminal' : 'Close terminal';
const getLaunchTargetTerminalNameLabel = (target) => {
    return truncateTerminalName(target.terminalName);
};
const getLaunchTargetTagLabels = (target) => [
    getLaunchTargetTerminalNameLabel(target),
    getLaunchTargetDirectoryLabel(target),
    getLaunchTargetTerminalLabel(target)
];
const sortLaunchTargetsByGroup = (targets) => [...targets].sort((left, right) => Number(right.keepTerminalOpen) - Number(left.keepTerminalOpen));
const buildLaunchTargets = (settings) => {
    const targets = [];
    for (const configuredCommand of settings.commands) {
        const name = configuredCommand.name.trim();
        const command = configuredCommand.command.trim();
        if (!name ||
            (configuredCommand.kind === 'shell-command' && !command)) {
            continue;
        }
        const configuredTerminalIndex = settings.terminals.findIndex((terminal) => terminal.id === configuredCommand.terminalId);
        const terminalIndex = configuredTerminalIndex >= 0 ? configuredTerminalIndex : 0;
        const terminal = settings.terminals[terminalIndex];
        const terminalName = terminal?.name.trim() || `Terminal ${terminalIndex + 1}`;
        targets.push({
            id: configuredCommand.kind === 'open-terminal'
                ? 'open-terminal'
                : `open-${configuredCommand.id}`,
            commandName: name,
            toolCommand: configuredCommand.kind === 'open-terminal' ? undefined : command,
            workingDirectory: configuredCommand.workingDirectory,
            keepTerminalOpen: configuredCommand.kind === 'open-terminal'
                ? true
                : configuredCommand.keepTerminalOpen,
            terminalId: terminal?.id ?? configuredCommand.terminalId,
            terminalName
        });
    }
    return targets;
};

const getCommandDetails = (target) => target.toolCommand ?? 'Open terminal';
class TerminalCommandMenu extends obsidian.FuzzySuggestModal {
    targets;
    onChoose;
    constructor(app, targets, onChoose) {
        super(app);
        this.targets = targets;
        this.onChoose = onChoose;
        this.setPlaceholder('Search commands…');
        this.setInstructions([
            { command: '↑↓', purpose: 'to navigate' },
            { command: '↵', purpose: 'to run' },
            { command: 'esc', purpose: 'to dismiss' }
        ]);
    }
    getItems() {
        return sortLaunchTargetsByGroup(this.targets);
    }
    getItemText(target) {
        return `${target.terminalName} ${getLaunchTargetDirectoryLabel(target)} ${getLaunchTargetTerminalLabel(target)} ${target.commandName} ${getCommandDetails(target)}`;
    }
    renderSuggestion(match, el) {
        const target = match.item;
        const details = getCommandDetails(target);
        el.addClass('terminal-commands-menu-item');
        const headingEl = el.createDiv({ cls: 'terminal-commands-menu-heading' });
        headingEl.createDiv({ cls: 'terminal-commands-menu-name', text: target.commandName });
        const tagsEl = headingEl.createDiv({ cls: 'terminal-commands-menu-tags' });
        const [terminalNameLabel, directoryLabel, terminalBehaviorLabel] = getLaunchTargetTagLabels(target);
        const terminalNameTagEl = tagsEl.createSpan({
            cls: 'terminal-commands-menu-tag terminal-commands-menu-tag-terminal-name',
            text: terminalNameLabel
        });
        terminalNameTagEl.setAttr('title', target.terminalName);
        tagsEl.createSpan({
            cls: 'terminal-commands-menu-tag terminal-commands-menu-tag-directory',
            text: directoryLabel
        });
        tagsEl.createSpan({
            cls: 'terminal-commands-menu-tag terminal-commands-menu-tag-terminal-behavior',
            text: terminalBehaviorLabel
        });
        const detailsEl = el.createDiv({ cls: 'terminal-commands-menu-details', text: details });
        detailsEl.setAttr('title', details);
    }
    onChooseItem(target) {
        this.onChoose(target);
    }
}

const resolveCommandManager = (app) => {
    const maybeCommands = app.commands;
    if (maybeCommands &&
        typeof maybeCommands.findCommand === 'function' &&
        typeof maybeCommands.removeCommand === 'function') {
        return maybeCommands;
    }
    return null;
};

const sanitizeTerminalApp = (value) => value.trim();
const quotePosix = (value) => `'${value.replace(/'/g, `'"'"'`)}'`;
const quoteCmdPath = (value) => `"${value.replace(/"/g, '""')}"`;
const quotePowerShellPath = (value) => `'${value.replace(/'/g, "''")}'`;
const quoteWindowsExecutable = (value) => /[\s&(){}^=;!'+,`~]/.test(value) ? quoteCmdPath(value) : value;
const getWindowsTerminalKind = (value) => {
    const executableName = node_path.win32.basename(sanitizeTerminalApp(value)).toLowerCase();
    if (executableName === 'cmd' || executableName === 'cmd.exe') {
        return 'cmd';
    }
    if (executableName === 'powershell' || executableName === 'powershell.exe') {
        return 'powershell';
    }
    if (executableName === 'pwsh' || executableName === 'pwsh.exe') {
        return 'pwsh';
    }
    return null;
};
const isSupportedWindowsTerminalApp = (value) => getWindowsTerminalKind(value) !== null;
const ensureTempScript = (content) => {
    const dir = node_fs.mkdtempSync(node_path.join(node_os.tmpdir(), 'terminal-commands-'));
    const filePath = node_path.join(dir, 'launch.command');
    try {
        node_fs.writeFileSync(filePath, content, { mode: 0o755 });
    }
    catch (error) {
        node_fs.rmSync(dir, { recursive: true, force: true });
        throw error;
    }
    const cleanup = () => {
        try {
            node_fs.rmSync(dir, { recursive: true, force: true });
        }
        catch (error) {
            console.warn('[terminal-commands] Failed to remove temporary launch script', error);
        }
    };
    return { path: filePath, cleanup };
};
const buildMacLaunch = (terminalApp, vaultPath, toolCommand, options) => {
    const app = sanitizeTerminalApp(terminalApp);
    if (!app) {
        return null;
    }
    const openFlag = options?.reuseExistingMacApp === false ? '-na' : '-a';
    if (!toolCommand) {
        return {
            executable: 'open',
            args: [openFlag, app, vaultPath],
            cwd: vaultPath
        };
    }
    const scriptLines = ['#!/bin/bash', `cd -- ${quotePosix(vaultPath)}`, toolCommand];
    if (options?.keepTerminalOpen !== false) {
        scriptLines.push('exec "$SHELL"');
    }
    const { path, cleanup } = ensureTempScript(scriptLines.join('\n'));
    return {
        executable: 'open',
        args: [openFlag, app, path],
        cwd: vaultPath,
        cleanup
    };
};
const buildWindowsLaunch = (terminalApp, vaultPath, toolCommand, options) => {
    const app = sanitizeTerminalApp(terminalApp);
    if (!app) {
        return null;
    }
    const terminalKind = getWindowsTerminalKind(app);
    if (!terminalKind) {
        return null;
    }
    const executable = quoteWindowsExecutable(app);
    const cmdBody = `cd /d ${quoteCmdPath(vaultPath)}${toolCommand ? ` && ${toolCommand}` : ''}`;
    const cmdMode = options?.keepTerminalOpen === false ? '/C' : '/K';
    if (terminalKind === 'cmd') {
        return {
            executable: `start "" ${executable} ${cmdMode} "${cmdBody}"`,
            args: [],
            cwd: vaultPath,
            shell: true
        };
    }
    if (terminalKind === 'powershell' || terminalKind === 'pwsh') {
        const powerShellBody = `Set-Location -LiteralPath ${quotePowerShellPath(vaultPath)}${toolCommand ? `; ${toolCommand}` : ''}`;
        return {
            executable: `start "" ${executable}${options?.keepTerminalOpen === false ? '' : ' -NoExit'} -Command "${powerShellBody}"`,
            args: [],
            cwd: vaultPath,
            shell: true
        };
    }
    return null;
};
const buildUnixLaunch = (terminalApp, vaultPath, toolCommand, options) => {
    const app = sanitizeTerminalApp(terminalApp);
    if (!app) {
        return null;
    }
    if (!toolCommand) {
        return {
            executable: app,
            args: [],
            cwd: vaultPath
        };
    }
    const shellCommand = options?.keepTerminalOpen === false ? toolCommand : `${toolCommand}; exec "$SHELL"`;
    return {
        executable: app,
        args: app.includes('gnome-terminal')
            ? ['--', 'bash', '-lc', shellCommand]
            : ['-e', 'bash', '-lc', shellCommand],
        cwd: vaultPath
    };
};
const buildLaunchCommandForPlatform = (platform, terminalApp, vaultPath, toolCommand, options) => {
    if (platform === 'macos') {
        return buildMacLaunch(terminalApp, vaultPath, toolCommand, options);
    }
    if (platform === 'windows') {
        return buildWindowsLaunch(terminalApp, vaultPath, toolCommand, options);
    }
    return buildUnixLaunch(terminalApp, vaultPath, toolCommand, options);
};
const buildLaunchCommand = (terminalApp, vaultPath, toolCommand, options) => {
    if (!obsidian.Platform.isDesktopApp) {
        return null;
    }
    if (obsidian.Platform.isMacOS) {
        return buildLaunchCommandForPlatform('macos', terminalApp, vaultPath, toolCommand, options);
    }
    if (obsidian.Platform.isWin) {
        return buildLaunchCommandForPlatform('windows', terminalApp, vaultPath, toolCommand, options);
    }
    return buildLaunchCommandForPlatform('unix', terminalApp, vaultPath, toolCommand, options);
};

const SAVE_DELAY_MS = 250;
const TERMINAL_DROPDOWN_WIDTH = '112px';
const TERMINAL_COLUMN_HEADERS = [
    ['Name', false],
    ['Path', false],
    ['Browse', true],
    ['Delete', true]
];
const COMMAND_COLUMN_HEADERS = [
    ['Sort', true],
    ['Name', false],
    ['Command', false],
    ['Terminal', false],
    ['Note folder', true],
    ['Keep open', true],
    ['Delete', true]
];
class ConfirmModal extends obsidian.Modal {
    options;
    constructor(app, options) {
        super(app);
        this.options = options;
    }
    onOpen() {
        this.setTitle(this.options.title);
        this.contentEl.createEl('p', {
            text: this.options.message
        });
        const actions = new obsidian.Setting(this.contentEl);
        actions.settingEl.addClass('terminal-commands-confirm-actions');
        actions.addButton((button) => {
            button.setButtonText('Cancel').onClick(() => this.close());
            button.buttonEl.focus();
        });
        actions.addButton((button) => button
            .setButtonText(this.options.confirmLabel)
            .setDestructive()
            .onClick(() => {
            this.close();
            this.options.onConfirm();
        }));
    }
    onClose() {
        this.contentEl.empty();
    }
}
class TerminalCommandsSettingTab extends obsidian.PluginSettingTab {
    plugin;
    commandListObserver = null;
    saveTimer = null;
    constructor(app, plugin) {
        super(app, plugin);
        this.plugin = plugin;
    }
    getSettingDefinitions() {
        const definitions = [];
        if (obsidian.Platform.isMacOS) {
            definitions.push({
                type: 'group',
                heading: 'Terminal integration',
                items: [
                    {
                        name: 'Reuse existing terminal instance',
                        desc: 'Reuse the configured macOS terminal app instead of launching a new instance.',
                        visible: obsidian.Platform.isMacOS,
                        control: {
                            type: 'toggle',
                            key: 'reuseExistingMacApp'
                        }
                    }
                ]
            });
        }
        definitions.push(this.getTerminalDefinitions(), this.getCommandDefinitions());
        this.observeCommandList();
        return definitions;
    }
    hide() {
        this.flushScheduledSave();
    }
    dispose() {
        this.commandListObserver?.disconnect();
        this.commandListObserver = null;
        this.flushScheduledSave();
    }
    getTerminalDefinitions() {
        return {
            type: 'list',
            heading: 'Terminals',
            cls: 'terminal-commands-terminals-list',
            emptyState: 'At least one terminal is required.',
            addItem: {
                name: 'Add terminal',
                action: () => {
                    void this.addTerminal();
                }
            },
            onDelete: (index) => {
                const terminal = this.plugin.settings.terminals[index];
                if (terminal) {
                    this.confirmTerminalDelete(terminal, index);
                }
            },
            items: this.plugin.settings.terminals.map((terminal, index) => ({
                name: terminal.id,
                searchable: false,
                render: (setting) => {
                    this.renderTerminalControls(setting, terminal, index);
                }
            }))
        };
    }
    getCommandDefinitions() {
        return {
            type: 'list',
            heading: 'Commands',
            cls: 'terminal-commands-list',
            emptyState: 'No commands. Add one to create a command palette entry.',
            addItem: {
                name: 'Add command',
                action: () => {
                    void this.addCommand();
                }
            },
            onReorder: (oldIndex, newIndex) => {
                const commands = this.plugin.settings.commands;
                const [movedCommand] = commands.splice(oldIndex, 1);
                if (!movedCommand) {
                    return;
                }
                commands.splice(newIndex, 0, movedCommand);
                void this.saveImmediately();
            },
            onDelete: (index) => {
                const command = this.plugin.settings.commands[index];
                if (command) {
                    this.confirmCommandDelete(command, index);
                }
            },
            items: this.plugin.settings.commands.map((command, index) => ({
                name: command.id,
                searchable: false,
                render: (setting) => {
                    this.renderCommandControls(setting, command, index);
                }
            }))
        };
    }
    renderCommandControls(setting, command, index) {
        setting.settingEl.addClass('terminal-commands-command-setting');
        setting.settingEl.toggleClass('is-open-terminal', command.kind === 'open-terminal');
        setting.settingEl.setAttribute('aria-label', command.name.trim() || `Command ${index + 1}`);
        setting.infoEl.remove();
        setting.controlEl.addClass('terminal-commands-command-controls');
        setting.addText((text) => {
            text.setPlaceholder('Name').setValue(command.name).onChange((value) => {
                command.name = value;
                this.scheduleSave();
            });
            text.inputEl.setAttribute('aria-label', 'Command palette name');
        });
        setting.addText((text) => {
            if (command.kind === 'open-terminal') {
                text.setValue('').setDisabled(true);
            }
            else {
                text.setPlaceholder('Command').setValue(command.command).onChange((value) => {
                    command.command = value;
                    this.scheduleSave();
                });
            }
            text.inputEl.setAttribute('aria-label', 'Shell command');
        });
        setting.addDropdown((dropdown) => {
            this.plugin.settings.terminals.forEach((terminal, terminalIndex) => {
                dropdown.addOption(terminal.id, this.getTerminalDropdownLabel(terminal, terminalIndex));
            });
            dropdown.setValue(command.terminalId).onChange((value) => {
                command.terminalId = value;
                this.setTerminalDropdownTitle(dropdown.selectEl, value);
                void this.saveImmediately();
            });
            dropdown.selectEl.setAttribute('aria-label', 'Terminal');
            dropdown.selectEl.addClass('terminal-commands-terminal-dropdown');
            dropdown.selectEl.setCssProps({
                '--dropdown-fitted-width': TERMINAL_DROPDOWN_WIDTH
            });
            this.setTerminalDropdownTitle(dropdown.selectEl, command.terminalId);
        });
        setting.addToggle((toggle) => {
            toggle
                .setValue(command.workingDirectory === 'current-note')
                .setTooltip('Use current note folder')
                .onChange((value) => {
                command.workingDirectory = value ? 'current-note' : 'vault';
                void this.saveImmediately();
            });
            toggle.toggleEl.setAttribute('aria-label', 'Use current note folder');
        });
        setting.addToggle((toggle) => {
            toggle
                .setValue(command.kind === 'open-terminal' ? true : command.keepTerminalOpen)
                .setDisabled(command.kind === 'open-terminal')
                .setTooltip('Keep terminal open')
                .onChange((value) => {
                if (command.kind === 'open-terminal') {
                    return;
                }
                command.keepTerminalOpen = value;
                void this.saveImmediately();
            });
            toggle.toggleEl.setAttribute('aria-label', 'Keep terminal open');
        });
        setting.controlEl.ownerDocument.defaultView?.queueMicrotask(() => {
            const dragHandle = setting.controlEl.querySelector('.mod-drag-handle');
            if (dragHandle) {
                setting.controlEl.prepend(dragHandle);
            }
            if (command.kind === 'open-terminal') {
                setting.controlEl
                    .querySelector('.mod-delete')
                    ?.remove();
            }
        });
    }
    renderTerminalControls(setting, terminal, index) {
        setting.settingEl.addClass('terminal-commands-terminal-setting');
        setting.settingEl.setAttribute('aria-label', this.getTerminalLabel(terminal, index));
        setting.infoEl.remove();
        setting.controlEl.addClass('terminal-commands-terminal-controls');
        setting.addText((text) => {
            text.setPlaceholder('Name').setValue(terminal.name).onChange((value) => {
                terminal.name = value;
                this.scheduleSave();
            });
            text.inputEl.setAttribute('aria-label', 'Terminal name');
            text.inputEl.addEventListener('blur', () => this.update());
        });
        let pathInput = null;
        setting.addText((text) => {
            text.setPlaceholder('Select an executable').setValue(getCurrentTerminalApp(terminal.applications));
            text.inputEl.readOnly = true;
            pathInput = text.inputEl;
            text.inputEl.setAttribute('aria-label', 'Terminal application');
        });
        const fileInput = setting.controlEl.createEl('input', {
            cls: 'terminal-commands-terminal-file-input',
            attr: { type: 'file', 'aria-hidden': 'true', tabIndex: '-1' }
        });
        if (obsidian.Platform.isWin) {
            fileInput.accept = '.exe';
        }
        fileInput.addEventListener('change', () => {
            const file = fileInput.files?.[0];
            if (!file) {
                return;
            }
            const executablePath = electron.webUtils.getPathForFile(file);
            if (!executablePath) {
                new obsidian.Notice('Unable to read the selected executable path.');
                return;
            }
            if (obsidian.Platform.isWin && !executablePath.toLowerCase().endsWith('.exe')) {
                new obsidian.Notice('Select a Windows .exe file.');
                return;
            }
            if (obsidian.Platform.isWin && !isSupportedWindowsTerminalApp(executablePath)) {
                new obsidian.Notice('Supported Windows terminals are cmd.exe, powershell.exe, and pwsh.exe.');
                return;
            }
            terminal.applications = setCurrentTerminalApp(terminal.applications, executablePath);
            if (pathInput) {
                pathInput.value = executablePath;
            }
            fileInput.value = '';
            void this.saveImmediately();
        });
        setting.addExtraButton((button) => {
            button
                .setIcon('folder-open')
                .setTooltip('Select terminal executable')
                .onClick(() => fileInput.click());
        });
    }
    async addCommand() {
        const command = createCommand(this.plugin.settings.commands, this.plugin.settings.terminals[0]?.id ?? '');
        this.plugin.settings.commands.push(command);
        await this.saveImmediately();
        this.update();
    }
    async addTerminal() {
        this.plugin.settings.terminals.push(createTerminalProfile(this.plugin.settings.terminals));
        await this.saveImmediately();
        this.update();
    }
    confirmCommandDelete(command, index) {
        if (command.kind === 'open-terminal') {
            new obsidian.Notice('Open in terminal cannot be deleted.');
            return;
        }
        const displayName = command.name.trim() || `Command ${index + 1}`;
        new ConfirmModal(this.app, {
            title: 'Delete command',
            message: `Delete "${displayName}"? This action cannot be undone.`,
            confirmLabel: 'Delete',
            onConfirm: () => {
                const currentIndex = this.plugin.settings.commands.findIndex((candidate) => candidate.id === command.id);
                if (currentIndex < 0) {
                    return;
                }
                this.plugin.settings.commands.splice(currentIndex, 1);
                void this.saveImmediately().then(() => this.update());
            }
        }).open();
    }
    confirmTerminalDelete(terminal, index) {
        if (this.plugin.settings.terminals.length <= 1) {
            new obsidian.Notice('At least one terminal is required.');
            return;
        }
        const displayName = this.getTerminalLabel(terminal, index);
        new ConfirmModal(this.app, {
            title: 'Delete terminal',
            message: `Delete "${displayName}"? This action cannot be undone.`,
            confirmLabel: 'Delete',
            onConfirm: () => {
                const terminalIndex = this.plugin.settings.terminals.findIndex((candidate) => candidate.id === terminal.id);
                if (terminalIndex < 0) {
                    return;
                }
                this.plugin.settings.terminals.splice(terminalIndex, 1);
                const fallbackTerminalId = this.plugin.settings.terminals[0]?.id ?? '';
                for (const command of this.plugin.settings.commands) {
                    if (command.terminalId === terminal.id) {
                        command.terminalId = fallbackTerminalId;
                    }
                }
                void this.saveImmediately().then(() => this.update());
            }
        }).open();
    }
    confirmRestoreTerminals() {
        new ConfirmModal(this.app, {
            title: 'Restore default terminals',
            message: 'Replace the terminal list with the platform defaults? Custom terminals will be removed, and their commands will use the first default terminal.',
            confirmLabel: 'Restore',
            onConfirm: () => {
                restoreDefaultTerminalProfiles(this.plugin.settings);
                void this.saveImmediately().then(() => this.update());
            }
        }).open();
    }
    getTerminalLabel(terminal, index) {
        return terminal.name.trim() || `Terminal ${index + 1}`;
    }
    getTerminalDropdownLabel(terminal, index) {
        return truncateTerminalName(this.getTerminalLabel(terminal, index));
    }
    setTerminalDropdownTitle(selectEl, terminalId) {
        const terminalIndex = this.plugin.settings.terminals.findIndex((terminal) => terminal.id === terminalId);
        const terminal = this.plugin.settings.terminals[terminalIndex];
        if (terminal) {
            selectEl.setAttribute('title', this.getTerminalLabel(terminal, terminalIndex));
        }
        else {
            selectEl.removeAttribute('title');
        }
    }
    observeCommandList() {
        if (!this.commandListObserver) {
            const ViewMutationObserver = this.containerEl.ownerDocument.defaultView?.MutationObserver;
            if (ViewMutationObserver) {
                this.commandListObserver = new ViewMutationObserver(() => {
                    this.addCommandListChrome();
                });
                this.commandListObserver.observe(this.containerEl, {
                    childList: true,
                    subtree: true
                });
            }
        }
        this.addCommandListChrome();
    }
    addCommandListChrome() {
        const terminalGroupEl = this.containerEl.querySelector('.terminal-commands-terminals-list');
        const terminalHeadingEl = terminalGroupEl?.querySelector('.setting-item-heading');
        const terminalHeadingControlsEl = terminalHeadingEl?.querySelector('.setting-item-control');
        if (terminalHeadingControlsEl &&
            !terminalHeadingControlsEl.querySelector('.terminal-commands-restore-terminals')) {
            const restoreButton = new obsidian.ButtonComponent(terminalHeadingControlsEl)
                .setButtonText('Restore defaults')
                .setTooltip('Restore the platform default terminal list')
                .setClass('terminal-commands-restore-terminals')
                .onClick(() => this.confirmRestoreTerminals());
            terminalHeadingControlsEl.prepend(restoreButton.buttonEl);
        }
        if (terminalGroupEl &&
            terminalHeadingEl &&
            !terminalGroupEl.querySelector('.terminal-commands-group-description')) {
            const terminalDescriptionEl = terminalGroupEl.createDiv({
                cls: 'terminal-commands-group-description',
                text: this.getTerminalGroupDescription()
            });
            terminalHeadingEl.after(terminalDescriptionEl);
        }
        this.renderColumnHeaders(terminalGroupEl?.querySelector('.setting-items'), 'terminal-commands-terminal-column-headers', TERMINAL_COLUMN_HEADERS);
        const groupEl = this.containerEl.querySelector('.terminal-commands-list');
        if (!groupEl) {
            return;
        }
        const headingEl = groupEl.querySelector('.setting-item-heading');
        if (headingEl && !groupEl.querySelector('.terminal-commands-group-description')) {
            const descriptionEl = groupEl.createDiv({
                cls: 'terminal-commands-group-description'
            });
            descriptionEl.createDiv({
                text: 'Note folder: on uses the note folder; off uses the Vault folder.'
            });
            descriptionEl.createDiv({
                text: 'Keep open: on keeps the terminal open after the command finishes; off closes it.'
            });
            headingEl.after(descriptionEl);
        }
        this.renderColumnHeaders(groupEl.querySelector('.setting-items'), 'terminal-commands-column-headers', COMMAND_COLUMN_HEADERS);
    }
    renderColumnHeaders(listEl, className, columns) {
        if (!listEl || listEl.querySelector(`.${className}`)) {
            return;
        }
        const headersEl = listEl.createDiv({
            cls: className,
            attr: { role: 'row' }
        });
        for (const [label, centered] of columns) {
            headersEl.createDiv({
                cls: `terminal-commands-column-header${centered ? ' is-centered' : ''}`,
                text: label,
                attr: { role: 'columnheader' }
            });
        }
        listEl.prepend(headersEl);
    }
    getTerminalGroupDescription() {
        if (obsidian.Platform.isWin) {
            return 'Supported terminals: Command Prompt (cmd), Windows PowerShell, and PowerShell 7 (pwsh). Other .exe files are rejected.';
        }
        if (obsidian.Platform.isMacOS) {
            return 'Supported terminals: Terminal and terminal apps that can open .command scripts.';
        }
        if (obsidian.Platform.isLinux) {
            return 'Supported terminals: GNOME Terminal and terminals compatible with -e bash -lc.';
        }
        return 'Terminal launching is available in the Obsidian desktop app.';
    }
    scheduleSave() {
        if (this.saveTimer !== null) {
            window.clearTimeout(this.saveTimer);
        }
        this.saveTimer = window.setTimeout(() => {
            this.saveTimer = null;
            void this.plugin.saveSettings();
        }, SAVE_DELAY_MS);
    }
    flushScheduledSave() {
        if (this.saveTimer === null) {
            return;
        }
        window.clearTimeout(this.saveTimer);
        this.saveTimer = null;
        void this.plugin.saveSettings();
    }
    async saveImmediately() {
        if (this.saveTimer !== null) {
            window.clearTimeout(this.saveTimer);
            this.saveTimer = null;
        }
        await this.plugin.saveSettings();
    }
}

const TEMP_SCRIPT_CLEANUP_DELAY_MS = 30_000;
class TerminalCommandsPlugin extends obsidian.Plugin {
    registeredCommandIds = new Set();
    settings = { ...DEFAULT_SETTINGS };
    async onload() {
        await this.loadSettings();
        const settingTab = new TerminalCommandsSettingTab(this.app, this);
        this.addSettingTab(settingTab);
        this.register(() => settingTab.dispose());
        this.addRibbonIcon('terminal', 'Terminal commands', () => {
            this.openCommandMenu();
        });
        this.refreshCommands();
    }
    openCommandMenu() {
        const menu = new TerminalCommandMenu(this.app, buildLaunchTargets(this.settings), (target) => {
            this.launchTarget(target);
        });
        menu.open();
    }
    refreshCommands() {
        const commandManager = resolveCommandManager(this.app);
        if (commandManager) {
            for (const fullId of this.registeredCommandIds) {
                if (commandManager.findCommand(fullId)) {
                    commandManager.removeCommand(fullId);
                }
            }
        }
        this.registeredCommandIds.clear();
        for (const target of buildLaunchTargets(this.settings)) {
            this.addCommand({
                id: target.id,
                name: target.commandName,
                callback: () => {
                    this.launchTarget(target);
                }
            });
            this.registeredCommandIds.add(`${this.manifest.id}:${target.id}`);
        }
    }
    launchTarget(target) {
        this.runLaunchCommand(() => this.composeLaunchCommand(target.toolCommand, target.workingDirectory, target.keepTerminalOpen, target.terminalId), target.commandName);
    }
    composeLaunchCommand(toolCommand, workingDirectory = 'vault', keepTerminalOpen = true, terminalId = this.settings.terminals[0]?.id ?? '') {
        const adapter = this.app.vault.adapter;
        if (!(adapter instanceof obsidian.FileSystemAdapter)) {
            return null;
        }
        const vaultPath = adapter.getBasePath();
        const launchPath = this.getLaunchPath(vaultPath, workingDirectory);
        const terminal = resolveTerminalProfile(this.settings, terminalId);
        const terminalApp = terminal
            ? getCurrentTerminalApp(terminal.applications)
            : '';
        const launchCommand = buildLaunchCommand(terminalApp, launchPath, toolCommand, {
            reuseExistingMacApp: this.settings.reuseExistingMacApp,
            keepTerminalOpen
        });
        return launchCommand ? { ...launchCommand, cwd: launchPath } : null;
    }
    getLaunchPath(vaultPath, workingDirectory) {
        if (workingDirectory === 'vault') {
            return vaultPath;
        }
        const activeFile = this.app.workspace.getActiveFile();
        const folderPath = activeFile?.parent?.path;
        return folderPath ? node_path.join(vaultPath, folderPath) : vaultPath;
    }
    runLaunchCommand(buildCommand, label) {
        const launchCommand = buildCommand();
        if (!launchCommand) {
            new obsidian.Notice(`Unable to run ${label}. Check the Terminal Commands settings for the terminal application name.`);
            return;
        }
        this.executeShellCommand(launchCommand, label);
    }
    executeShellCommand(launchCommand, label) {
        try {
            const child = node_child_process.spawn(launchCommand.executable, launchCommand.args, {
                cwd: launchCommand.cwd,
                shell: launchCommand.shell ?? false,
                detached: true,
                stdio: 'ignore'
            });
            child.on('error', (error) => {
                this.reportLaunchError(launchCommand.executable, label, error);
            });
            child.unref();
        }
        catch (error) {
            this.reportLaunchError(launchCommand.executable, label, error);
        }
        finally {
            if (launchCommand.cleanup) {
                const cleanup = launchCommand.cleanup;
                window.setTimeout(() => {
                    try {
                        cleanup();
                    }
                    catch (error) {
                        console.warn('[terminal-commands] Cleanup after command failed', error);
                    }
                }, TEMP_SCRIPT_CLEANUP_DELAY_MS);
            }
        }
    }
    reportLaunchError(executable, label, error) {
        console.error(`[terminal-commands] Failed to run '${executable}':`, error);
        new obsidian.Notice(`Failed to run ${label}. Check the developer console for details.`);
    }
    async loadSettings() {
        this.settings = normalizeSettings(await this.loadData());
    }
    async saveSettings() {
        await this.saveData(this.settings);
        this.refreshCommands();
    }
}

module.exports = TerminalCommandsPlugin;
//# sourceMappingURL=main.js.map

/* nosourcemap */
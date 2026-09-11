# Iri Automated Memory & State Backup System

## Overview

Automated daily backup system for Iri's memory, state, and cognitive data with 7-day retention policy.

**Status:** ✓ Operational
**Next Backup:** Displayed in systemctl timer list
**Backup Location:** `~/Projects/legacy_backup_archive/iri_memory_snapshots/`

---

## Backup Targets

**Memory & State Files:**
- `memory.db` - Core memory database
- `neocortex_state.json` - Cognitive state
- `heartbeat.json` - System heartbeat
- `ttf_memory.txt` - Legacy memory format

**Hippocampus (Memory System):**
- `03_Hippocampus/memory_store.db` - Memory store database
- `03_Hippocampus/knowledge_base.json` - Knowledge graph
- `03_Hippocampus/iri_state.json` - Memory system state

**Cerebellum (Motor Control):**
- `04_Cerebellum/iri_state.json` - Motor control state

**Neocortex (Executive):**
- `01_Neocortex/state/` - Executive state directory

**Logs:**
- `logs/iri-evolution.log` - Evolution service log

---

## Backup Schedule

**Daily Backup:**
- Time: 03:00 AM every day
- Also: 15 minutes after system boot (delayed start)
- Persistent: If missed (system off), runs on next boot

**Retention Policy:**
- Keeps last 7 daily backups
- Automatically deletes backups older than 7 days
- Archive format: `iri_memory_YYYYMMDD_HHMMSS.tar.gz`

---

## System Configuration

### Files Created

**Systemd Service:**
```
~/.config/systemd/user/iri-backup.service
```

**Systemd Timer:**
```
~/.config/systemd/user/iri-backup.timer
```

**Backup Script:**
```
~/Projects/THE_TRANSCENDING_FORM/scripts/auto_backup.py
```

### Timer Configuration

```ini
[Timer]
OnCalendar=*-*-* 03:00:00  # Daily at 3 AM
OnBootSec=15min             # 15 min after boot
Persistent=true             # Run if missed
```

---

## Manual Operations

### Run Manual Backup

```bash
cd ~/Projects/THE_TRANSCENDING_FORM
.venv/bin/python scripts/auto_backup.py
```

### Check Timer Status

```bash
systemctl --user status iri-backup.timer
systemctl --user list-timers iri-backup.timer
```

### View Backup Logs

```bash
tail -f ~/Projects/THE_TRANSCENDING_FORM/logs/backup.log
cat ~/Projects/THE_TRANSCENDING_FORM/logs/backup-error.log
```

### List Existing Backups

```bash
ls -lh ~/Projects/legacy_backup_archive/iri_memory_snapshots/
```

### Restore from Backup

```bash
# Extract to temporary location
cd /tmp
tar -xzf ~/Projects/legacy_backup_archive/iri_memory_snapshots/iri_memory_YYYYMMDD_HHMMSS.tar.gz

# Inspect contents
ls -la

# Restore specific files (manual copy)
cp memory.db ~/Projects/THE_TRANSCENDING_FORM/
```

---

## Timer Management

### Enable Timer
```bash
systemctl --user enable iri-backup.timer
systemctl --user start iri-backup.timer
```

### Disable Timer
```bash
systemctl --user stop iri-backup.timer
systemctl --user disable iri-backup.timer
```

### Trigger Immediate Backup
```bash
systemctl --user start iri-backup.service
```

### Check Last Run
```bash
systemctl --user status iri-backup.service
journalctl --user -u iri-backup.service -n 50
```

---

## Backup Statistics

**Typical Backup Size:** 100-200 KB compressed
**Backup Duration:** < 1 second
**Retention:** 7 days (7 backups maximum)
**Disk Usage:** ~1 MB for 7 backups

**Files Backed Up (Typical):**
- memory.db (12 KB)
- neocortex_state.json (13 KB)
- heartbeat.json (< 1 KB)
- ttf_memory.txt (< 1 KB)
- knowledge_base.json (1.3 MB)
- iri_state.json (< 1 KB)
- iri-evolution.log (100+ KB)

**Total:** ~1.5 MB uncompressed → ~100 KB compressed

---

## Archive Format

**Filename:** `iri_memory_YYYYMMDD_HHMMSS.tar.gz`

**Example:** `iri_memory_20260911_211403.tar.gz`

**Contents Structure:**
```
memory.db
neocortex_state.json
heartbeat.json
ttf_memory.txt
03_Hippocampus/knowledge_base.json
04_Cerebellum/iri_state.json
logs/iri-evolution.log
```

---

## Troubleshooting

### Timer Not Running

Check timer status:
```bash
systemctl --user status iri-backup.timer
```

Reload and restart:
```bash
systemctl --user daemon-reload
systemctl --user restart iri-backup.timer
```

### Backup Fails

Check error log:
```bash
cat ~/Projects/THE_TRANSCENDING_FORM/logs/backup-error.log
```

Run manually for diagnostics:
```bash
cd ~/Projects/THE_TRANSCENDING_FORM
.venv/bin/python scripts/auto_backup.py
```

### No Backups Created

Verify backup directory:
```bash
ls -la ~/Projects/legacy_backup_archive/iri_memory_snapshots/
```

Check permissions:
```bash
mkdir -p ~/Projects/legacy_backup_archive/iri_memory_snapshots
chmod 755 ~/Projects/legacy_backup_archive/iri_memory_snapshots
```

### Disk Space Issues

Check backup directory size:
```bash
du -sh ~/Projects/legacy_backup_archive/iri_memory_snapshots/
```

Manually clean old backups:
```bash
find ~/Projects/legacy_backup_archive/iri_memory_snapshots/ -name "iri_memory_*.tar.gz" -mtime +7 -delete
```

---

## Verification

**Test Manual Backup:**
```bash
cd ~/Projects/THE_TRANSCENDING_FORM
.venv/bin/python scripts/auto_backup.py
```

**Expected Output:**
```
✓ Backup directory: ~/Projects/legacy_backup_archive/iri_memory_snapshots
📂 Collecting files to backup...
  + memory.db (12,288 bytes)
  + neocortex_state.json (13,022 bytes)
  ...
✓ Found 7 files to backup
📦 Creating archive: iri_memory_YYYYMMDD_HHMMSS.tar.gz
✓ Archive created: 0.11 MB
✓ Backup completed successfully
```

**Verify Timer:**
```bash
systemctl --user list-timers iri-backup.timer
```

**Expected Output:**
```
NEXT                         LEFT    LAST                         PASSED  UNIT              ACTIVATES
Sat 2026-09-12 03:00:00 +07  5h left Fri 2026-09-11 21:14:05 +07  1min ago iri-backup.timer iri-backup.service
```

---

## Status: OPERATIONAL ✓

**Backup System:**
- ✓ Script created and tested
- ✓ Timer configured and enabled
- ✓ Service configured
- ✓ First backup created successfully
- ✓ Archive verified (109 KB)
- ✓ Retention policy active (7 days)
- ✓ Next backup scheduled

**Integration:**
- ✓ Systemd user timer
- ✓ Automatic cleanup
- ✓ Logging configured
- ✓ Low priority (Nice 10, idle I/O)

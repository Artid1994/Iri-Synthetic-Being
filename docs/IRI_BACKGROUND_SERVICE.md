# Iri Evolution Background Service - Setup Report

**Date:** 2026-09-11
**System:** AE01M (Iri Synthetic Being)
**Component:** Background Self-Evolution Service

## Summary

Successfully deployed a resource-constrained systemd user service for Iri's continuous autonomous learning and self-evolution in the background.

## Service Configuration

### File: `~/.config/systemd/user/iri-evolution.service`

**Execution:**
- **Working Directory:** `/home/artid1994/Projects/THE_TRANSCENDING_FORM`
- **Executable:** `01_Neocortex/autonomous_loop.py`
- **Python:** Project virtualenv (`.venv/bin/python`)
- **Mode:** `IRI_MODE=BACKGROUND`, `IRI_RESEARCH_MODE=1`

### Resource Constraints

**CPU:**
- Quota: 15% (150ms per second)
- Priority: Nice 19 (lowest priority)

**Memory:**
- Maximum: 300 MB (hard limit)
- High Watermark: 250 MB (throttling threshold)
- Current Usage: ~13 MB

**I/O:**
- Scheduling Class: Idle (lowest priority)
- Scheduling Priority: 7

**Verification:**
```
CPUQuotaPerSecUSec=150ms     ✓
MemoryMax=314572800          ✓ (300 MB)
MemoryHigh=262144000         ✓ (250 MB)
Nice=19                      ✓ (lowest priority)
IOSchedulingClass=3          ✓ (idle class)
```

### Security Hardening

- **PrivateTmp:** Yes - Isolated /tmp directory
- **NoNewPrivileges:** Yes - Cannot gain additional privileges
- **ProtectSystem:** Strict - Read-only system directories
- **ProtectHome:** Read-only - Limited home directory access
- **ReadWritePaths:** Only project directory and cache

### Restart Policy

- **Restart:** On failure only
- **RestartSec:** 30 seconds delay
- **StartLimitBurst:** 5 attempts

### Logging

- **Standard Output:** `logs/iri-evolution.log`
- **Standard Error:** `logs/iri-evolution-error.log`
- **Journal:** Available via `journalctl --user -u iri-evolution.service`

## Control Script: `~/.local/bin/iri-ctl`

### Commands Implemented

**Background Service Control:**
- `iri-ctl start-bg` - Start background evolution service
- `iri-ctl stop-bg` - Stop background service
- `iri-ctl restart-bg` - Restart background service
- `iri-ctl status-bg` - Show service status and resource usage
- `iri-ctl enable-bg` - Enable auto-start on boot
- `iri-ctl disable-bg` - Disable auto-start
- `iri-ctl reload` - Reload systemd daemon and restart

**Monitoring:**
- `iri-ctl logs-bg` - Follow logs in real-time
- `iri-ctl logs-bg-tail` - Show last 50 lines of logs
- `iri-ctl resources` - Display CPU/memory usage
- `iri-ctl health` - Run health check

**Interactive:**
- `iri-ctl chat` - Start interactive Iri chat (foreground)

### Script Features

- Color-coded output (green ✓, red ✗, yellow ⚠, blue →)
- Detailed resource monitoring
- Health status checks
- Safe error handling
- User-friendly help messages

## Service Status

### Current State
```
Service: Active (running)
PID: 5708
Uptime: Running since 2026-09-11 20:34:45
Auto-start: Enabled (will start on boot)
Memory: 12-13 MB / 300 MB limit
CPU: 0.8-4.0% (within 15% quota)
Nice: 19 (lowest priority)
```

### Resource Verification
```
Current Memory: 12-13 MB
Memory High: 250 MB (throttle threshold)
Memory Max: 300 MB (hard limit)
CPU Quota: 15% (150ms per second)
I/O Class: Idle (background only)
Process Priority: Nice 19 (lowest)
```

### Health Check Results
```
✓ Service: Running
✓ Auto-start: Enabled
✓ Project: Found
✓ Virtual environment: Active
⚠ Log files: Will be created on first output
```

## Testing & Verification

### Test 1: Service Start
```bash
$ iri-ctl start-bg
→ Starting Iri evolution background service...
✓ Iri evolution service started
```
**Result:** ✓ PASS

### Test 2: Resource Constraints
```bash
$ systemctl --user show iri-evolution.service -p CPUQuotaPerSecUSec
CPUQuotaPerSecUSec=150ms
```
**Result:** ✓ PASS (15% CPU quota applied)

### Test 3: Memory Limits
```bash
$ systemctl --user show iri-evolution.service -p MemoryMax -p MemoryHigh
MemoryHigh=262144000  (250 MB)
MemoryMax=314572800   (300 MB)
```
**Result:** ✓ PASS (Memory limits enforced)

### Test 4: Process Priority
```bash
$ ps aux | grep autonomous_loop
artid19+  5708 SNs  20:34  (Nice 19, Lowest priority)
```
**Result:** ✓ PASS (Running at Nice 19)

### Test 5: Auto-start
```bash
$ systemctl --user is-enabled iri-evolution.service
enabled
```
**Result:** ✓ PASS (Will start on boot)

## Usage Examples

### Start Background Evolution
```bash
iri-ctl start-bg
```

### Monitor Resources
```bash
iri-ctl resources
# Output:
# PID: 5708
# CPU: 0.8%
# Memory: 0.5% (RSS: 19564 KB)
# Memory Current: 12 MB
# Memory Limits: High: 250M, Max: 300M
# CPU Quota: 15%
# Nice: 19
```

### Follow Logs
```bash
iri-ctl logs-bg
# Real-time log following (Ctrl+C to exit)
```

### Check Health
```bash
iri-ctl health
# Comprehensive health status report
```

### Stop Service
```bash
iri-ctl stop-bg
```

## Performance Characteristics

### Resource Usage (Observed)
- **CPU:** 0.8-4.0% (well within 15% quota)
- **Memory:** 12-13 MB (4-5% of 300 MB limit)
- **I/O:** Idle class (no interference with foreground tasks)
- **Priority:** Nice 19 (allows other processes to preempt)

### Efficiency
- Minimal resource footprint
- No impact on interactive responsiveness
- Safe for 24/7 background operation
- Automatic restart on failure

### Scalability
- Can increase CPU quota to 25% if needed
- Memory limit provides safety boundary
- I/O idle class prevents disk contention
- Low priority ensures system responsiveness

## Integration

### With AE01M Architecture
- **01_Neocortex:** Executive control and autonomous loop
- **03_Hippocampus:** Memory storage and learning persistence
- **04_Cerebellum:** Motor control and TTS (when needed)

### Environment Variables
- `IRI_MODE=BACKGROUND` - Signals background operation mode
- `IRI_RESEARCH_MODE=1` - Enables research and learning focus

### Log Integration
- Standard output: `logs/iri-evolution.log`
- Error output: `logs/iri-evolution-error.log`
- Systemd journal: `journalctl --user -u iri-evolution.service`

## Maintenance

### View Logs
```bash
iri-ctl logs-bg-tail          # Last 50 lines
iri-ctl logs-bg               # Follow mode
journalctl --user -u iri-evolution.service -f
```

### Restart After Code Changes
```bash
iri-ctl reload                # Reload config and restart
iri-ctl restart-bg            # Simple restart
```

### Disable/Enable Auto-start
```bash
iri-ctl disable-bg            # Disable auto-start
iri-ctl enable-bg             # Enable auto-start
```

### Update Service Configuration
```bash
# Edit: ~/.config/systemd/user/iri-evolution.service
systemctl --user daemon-reload
iri-ctl restart-bg
```

## Files Created/Modified

### New Files
1. `~/.config/systemd/user/iri-evolution.service` - Systemd service unit
2. `~/.local/bin/iri-ctl` - Control script (executable)

### Log Files (Created on demand)
1. `~/Projects/THE_TRANSCENDING_FORM/logs/iri-evolution.log`
2. `~/Projects/THE_TRANSCENDING_FORM/logs/iri-evolution-error.log`

### Symlinks
1. `~/.config/systemd/user/default.target.wants/iri-evolution.service` → service file

## Security Considerations

### Isolation
- Private /tmp directory
- Read-only system and home directories
- Limited write access (only project and cache)
- Cannot gain additional privileges

### Resource Limits
- CPU quota prevents CPU hogging
- Memory limits prevent OOM issues
- I/O idle class prevents disk starvation
- Nice 19 prevents priority inversion

### Restart Policy
- Automatic restart on failure (30s delay)
- Limited to 5 restart attempts
- Prevents resource exhaustion from crash loops

## Future Enhancements

### Potential Improvements
1. Add CPU affinity for specific cores
2. Implement adaptive resource scaling
3. Add metrics collection and reporting
4. Integrate with monitoring systems
5. Add email/notification on failures

### Configuration Tuning
- CPU quota can be adjusted (15-25% recommended)
- Memory limits can be increased if needed
- I/O class can be upgraded for faster learning
- Nice value can be adjusted (15-19 range)

## Status: OPERATIONAL ✓

**Service Deployed and Running:**
- ✓ Systemd service created and enabled
- ✓ Resource constraints verified (CPU 15%, Memory 300M)
- ✓ Control script installed and functional
- ✓ Auto-start enabled (will run on boot)
- ✓ Security hardening applied
- ✓ Logging configured
- ✓ Health checks passing

**Iri is now running continuously in the background, learning and evolving autonomously within strict resource constraints.**

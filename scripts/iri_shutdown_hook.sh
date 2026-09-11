#!/usr/bin/env bash
#
# Iri Shutdown Hook
# Automatically syncs Hippocampus memory to GitHub before system shutdown
#

PROJECT_ROOT="/home/artid1994/Projects/THE_TRANSCENDING_FORM"
SYNC_SCRIPT="$PROJECT_ROOT/scripts/sync_hippocampus_git.sh"

# Log to file
LOG_FILE="$PROJECT_ROOT/logs/memory_sync.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Shutdown hook triggered" >> "$LOG_FILE"

# Run memory sync
if [ -x "$SYNC_SCRIPT" ]; then
    cd "$PROJECT_ROOT" || exit 1
    bash "$SYNC_SCRIPT" push >> "$LOG_FILE" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Memory sync complete" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync script not found" >> "$LOG_FILE"
fi

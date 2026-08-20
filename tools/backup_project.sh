#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_ROOT="$PROJECT_ROOT/.project_backups"

mkdir -p "$BACKUP_ROOT"

COMMIT="$(git -C "$PROJECT_ROOT" rev-parse HEAD)"
SHORT_COMMIT="$(git -C "$PROJECT_ROOT" rev-parse --short HEAD)"
BRANCH="$(git -C "$PROJECT_ROOT" branch --show-current)"
TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"

BACKUP_DIR="$BACKUP_ROOT/${TIMESTAMP}_${SHORT_COMMIT}"

mkdir -p "$BACKUP_DIR"

git -C "$PROJECT_ROOT" archive \
  --format=tar \
  HEAD \
  -o "$BACKUP_DIR/project_${SHORT_COMMIT}.tar"

git -C "$PROJECT_ROOT" rev-parse HEAD > "$BACKUP_DIR/COMMIT"
printf '%s\n' "$BRANCH" > "$BACKUP_DIR/BRANCH"
git -C "$PROJECT_ROOT" status --short > "$BACKUP_DIR/STATUS"

cat > "$BACKUP_DIR/MANIFEST" <<MANIFEST
The Transcending Form Project Backup

Timestamp: $TIMESTAMP
Branch: $BRANCH
Commit: $COMMIT
Short commit: $SHORT_COMMIT

Backup source:
- Git tracked files at HEAD only
- No .venv
- No ignored imported source
- No build/cache files

Recovery:
1. Extract project archive.
2. Verify COMMIT.
3. Restore dependencies separately.
4. Run the project's test suite.
MANIFEST

printf '\n=== BACKUP CREATED ===\n'
printf 'Path: %s\n' "$BACKUP_DIR"
printf 'Commit: %s\n' "$COMMIT"
printf 'Branch: %s\n' "$BRANCH"
printf 'Size: '
du -sh "$BACKUP_DIR" | cut -f1

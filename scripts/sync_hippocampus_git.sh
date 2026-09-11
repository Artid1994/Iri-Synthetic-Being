#!/usr/bin/env bash
#
# Hippocampus Memory Git Synchronization
# Automates push/pull of memory state to GitHub for cross-device continuity
#

set -e

PROJECT_ROOT="/home/artid1994/Projects/THE_TRANSCENDING_FORM"
HIPPOCAMPUS_DIR="03_Hippocampus"
MEMORY_BRANCH="${IRI_MEMORY_BRANCH:-checkpoint/130-tests-pass}"
REMOTE_NAME="${IRI_MEMORY_REMOTE:-origin}"
DEFAULT_REMOTE_URL="https://github.com/Artid1994/Iri-Synthetic-Being.git"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[Memory Sync]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[Memory Sync]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[Memory Sync]${NC} $1"
}

log_error() {
    echo -e "${RED}[Memory Sync]${NC} $1"
}

# Change to project root
cd "$PROJECT_ROOT" || {
    log_error "Failed to change to project root: $PROJECT_ROOT"
    exit 1
}

# Check if git repository
if [ ! -d ".git" ]; then
    log_error "Not a git repository. Run 'git init' first."
    exit 1
fi

# Function: Pull memory updates from remote
pull_memory() {
    log_info "Pulling memory updates from remote..."
    
    # Fetch remote changes
    if ! git fetch "$REMOTE_NAME" "$MEMORY_BRANCH" 2>/dev/null; then
        log_warning "Failed to fetch from remote (may not exist yet)"
        return 1
    fi
    
    # Check if there are remote changes
    LOCAL=$(git rev-parse "@" 2>/dev/null || echo "none")
    REMOTE=$(git rev-parse "@{u}" 2>/dev/null || echo "none")
    
    if [ "$LOCAL" = "$REMOTE" ]; then
        log_success "Memory already up-to-date"
        return 0
    fi
    
    # Stash local changes if any
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        log_info "Stashing local changes..."
        git stash push -m "Auto-stash before memory pull $(date +%Y%m%d_%H%M%S)"
    fi
    
    # Pull with rebase to maintain linear history
    if git pull --rebase "$REMOTE_NAME" "$MEMORY_BRANCH"; then
        log_success "Memory pulled successfully"
        
        # Pop stash if it exists
        if git stash list | grep -q "Auto-stash"; then
            log_info "Restoring local changes..."
            git stash pop
        fi
        return 0
    else
        log_error "Pull failed - manual intervention required"
        return 1
    fi
}

# Function: Push memory updates to remote
push_memory() {
    log_info "Pushing memory updates to remote..."
    
    # Check for changes in Hippocampus
    if git diff --quiet "$HIPPOCAMPUS_DIR" && \
       git diff --cached --quiet "$HIPPOCAMPUS_DIR"; then
        log_success "No memory changes to sync"
        return 0
    fi
    
    # Stage Hippocampus changes
    log_info "Staging Hippocampus changes..."
    git add "$HIPPOCAMPUS_DIR/"
    
    # Check if there are staged changes
    if git diff --cached --quiet; then
        log_success "No staged changes to commit"
        return 0
    fi
    
    # Create commit
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')
    COMMIT_MSG="Auto-sync Hippocampus memory [$TIMESTAMP]

Changed files:
$(git diff --cached --name-only "$HIPPOCAMPUS_DIR" | sed 's/^/  - /')

Automated memory synchronization by Iri (AE01M)"
    
    log_info "Creating commit..."
    if git commit -m "$COMMIT_MSG"; then
        log_success "Commit created"
    else
        log_error "Commit failed"
        return 1
    fi
    
    # Push to remote
    log_info "Pushing to remote..."
    if git push "$REMOTE_NAME" "$MEMORY_BRANCH"; then
        log_success "Memory synced successfully to GitHub"
        return 0
    else
        log_error "Push failed - check network and credentials"
        return 1
    fi
}

# Function: Show sync status
status() {
    log_info "Memory Sync Status"
    echo ""
    echo "Repository: $(git remote get-url $REMOTE_NAME 2>/dev/null || echo 'No remote configured')"
    echo "Branch: $MEMORY_BRANCH"
    echo "Last commit: $(git log -1 --format='%h - %s (%ar)' 2>/dev/null || echo 'No commits')"
    echo ""
    echo "Hippocampus changes:"
    
    if git diff --quiet "$HIPPOCAMPUS_DIR" && \
       git diff --cached --quiet "$HIPPOCAMPUS_DIR"; then
        echo "  No uncommitted changes"
    else
        git status --short "$HIPPOCAMPUS_DIR"
    fi
    echo ""
}

# Function: Setup GitHub sync
setup() {
    log_info "Setting up GitHub Memory Sync"
    echo ""
    
    # Check if remote exists
    if git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
        log_warning "Remote '$REMOTE_NAME' already configured:"
        echo "  $(git remote get-url $REMOTE_NAME)"
        echo ""
        read -p "Reconfigure? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Setup cancelled"
            return 0
        fi
        git remote remove "$REMOTE_NAME"
    fi
    
    # Get repository URL
    echo "Enter GitHub repository URL:"
    echo "  SSH: git@github.com:username/repo.git"
    echo "  HTTPS: https://github.com/username/repo.git"
    read -p "URL: " REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        log_error "No URL provided"
        return 1
    fi
    
    # Add remote
    if git remote add "$REMOTE_NAME" "$REPO_URL"; then
        log_success "Remote added: $REPO_URL"
    else
        log_error "Failed to add remote"
        return 1
    fi
    
    # Test connection
    log_info "Testing connection..."
    if git fetch "$REMOTE_NAME" 2>/dev/null; then
        log_success "Connection successful"
    else
        log_warning "Could not fetch from remote (repository may be empty)"
    fi
    
    echo ""
    log_success "Setup complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Ensure SSH key or PAT is configured"
    echo "  2. Run: $0 push"
    echo ""
}

# Main command router
case "${1:-status}" in
    pull)
        pull_memory
        ;;
    push)
        push_memory
        ;;
    sync)
        # Full sync: pull then push
        log_info "Full sync: pull + push"
        pull_memory
        push_memory
        ;;
    status)
        status
        ;;
    setup)
        setup
        ;;
    *)
        echo "Hippocampus Memory Git Synchronization"
        echo ""
        echo "Usage: $0 {pull|push|sync|status|setup}"
        echo ""
        echo "Commands:"
        echo "  pull    Pull memory updates from GitHub"
        echo "  push    Push local memory changes to GitHub"
        echo "  sync    Full synchronization (pull + push)"
        echo "  status  Show current sync status"
        echo "  setup   Configure GitHub remote"
        echo ""
        echo "Environment variables:"
        echo "  IRI_MEMORY_BRANCH  Branch name (default: main)"
        echo "  IRI_MEMORY_REMOTE  Remote name (default: origin)"
        exit 1
        ;;
esac

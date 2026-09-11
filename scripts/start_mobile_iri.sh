#!/usr/bin/env bash
#
# Mobile Iri Launch Script (Termux/Android)
# Pulls latest memory from GitHub and starts lightweight CLI loop
#

set -e

# Detect environment
if [[ -n "$PREFIX" ]] && [[ "$PREFIX" == *"com.termux"* ]]; then
    IS_TERMUX=true
    PROJECT_ROOT="$HOME/storage/shared/Projects/THE_TRANSCENDING_FORM"
else
    IS_TERMUX=false
    PROJECT_ROOT="${PROJECT_ROOT:-$HOME/Projects/THE_TRANSCENDING_FORM}"
fi

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[Iri Mobile]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[Iri Mobile]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[Iri Mobile]${NC} $1"
}

echo "========================================"
echo "  Iri (AE01M) - Mobile Launch"
echo "========================================"
echo ""

# Check project directory
if [ ! -d "$PROJECT_ROOT" ]; then
    log_warning "Project directory not found: $PROJECT_ROOT"
    log_info "Clone repository first:"
    echo "  git clone <your-repo-url> $PROJECT_ROOT"
    exit 1
fi

cd "$PROJECT_ROOT" || exit 1

# Sync memory from GitHub
log_info "Syncing memory from GitHub..."
if [ -x "scripts/sync_hippocampus_git.sh" ]; then
    if bash scripts/sync_hippocampus_git.sh pull; then
        log_success "Memory synchronized"
    else
        log_warning "Memory sync failed - continuing with local state"
    fi
else
    log_warning "Sync script not found - skipping memory pull"
fi

echo ""

# Detect Python
if [ "$IS_TERMUX" = true ]; then
    PYTHON_BIN="python"
else
    if [ -f ".venv/bin/python" ]; then
        PYTHON_BIN=".venv/bin/python"
    else
        PYTHON_BIN="python3"
    fi
fi

# Check Python availability
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    log_warning "Python not found. Install it first:"
    if [ "$IS_TERMUX" = true ]; then
        echo "  pkg install python"
    else
        echo "  sudo apt install python3 python3-venv"
    fi
    exit 1
fi

# Install dependencies (Termux)
if [ "$IS_TERMUX" = true ]; then
    log_info "Checking Termux dependencies..."
    
    # Essential packages
    REQUIRED_PKGS="git python"
    for pkg in $REQUIRED_PKGS; do
        if ! command -v "$pkg" &> /dev/null; then
            log_warning "$pkg not installed"
            read -p "Install $pkg? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                pkg install -y "$pkg"
            fi
        fi
    done
fi

# Launch mode selection
echo ""
log_info "Select launch mode:"
echo "  1. Interactive Chat (iri-ctl chat)"
echo "  2. Status Check (iri-ctl status)"
echo "  3. Autonomous Loop (lightweight, experimental)"
echo "  4. Exit"
echo ""
read -p "Select [1-4]: " -n 1 -r MODE
echo ""
echo ""

case $MODE in
    1)
        log_info "Launching interactive chat..."
        if [ -x "$HOME/.local/bin/iri-ctl" ]; then
            "$HOME/.local/bin/iri-ctl" chat
        elif [ -f "scripts/iri_chat.py" ]; then
            "$PYTHON_BIN" scripts/iri_chat.py
        else
            log_warning "Chat script not found"
            exit 1
        fi
        ;;
    2)
        log_info "System status..."
        if [ -x "$HOME/.local/bin/iri-ctl" ]; then
            "$HOME/.local/bin/iri-ctl" status
        else
            log_warning "iri-ctl not installed"
        fi
        ;;
    3)
        log_info "Starting autonomous loop (lightweight)..."
        log_warning "Autonomous mode requires LLM backend (ollama/gemma)"
        log_warning "Not yet implemented for mobile"
        exit 1
        ;;
    4)
        log_info "Goodbye!"
        exit 0
        ;;
    *)
        log_warning "Invalid selection"
        exit 1
        ;;
esac

# Sync memory back to GitHub on exit
echo ""
log_info "Syncing memory changes back to GitHub..."
if [ -x "scripts/sync_hippocampus_git.sh" ]; then
    bash scripts/sync_hippocampus_git.sh push
else
    log_warning "Sync script not found - memory not pushed"
fi

log_success "Session complete"

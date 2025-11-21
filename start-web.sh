#!/usr/bin/env bash
#
# start-web.sh - Start the web UI with proper port management
#
# This script handles:
# - Killing stale processes on the port
# - Finding an available port if default is taken
# - Proper cleanup on exit
#

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
DEFAULT_PORT=3000  # Common dev port, avoids macOS AirPlay (5000) and common proxies (8080)
MAX_PORT_ATTEMPTS=10
AUTO_OPEN_BROWSER=true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Helper Functions
# ============================================================================

log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✓${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $*"
}

log_error() {
    echo -e "${RED}✗${NC} $*" >&2
}

# Kill any process using the specified port
kill_port() {
    local port=$1

    log_info "Checking for processes on port $port..."

    # Find PIDs using the port (works on macOS and Linux)
    local pids
    if command -v lsof &>/dev/null; then
        pids=$(lsof -ti tcp:"$port" 2>/dev/null || true)
    else
        # Fallback for systems without lsof
        pids=$(netstat -vanp tcp 2>/dev/null | grep ".$port " | awk '{print $9}' | grep -v '\*' || true)
    fi

    if [[ -n "$pids" ]]; then
        log_warning "Found processes using port $port: $pids"
        log_warning "Killing stale processes..."

        for pid in $pids; do
            if kill -9 "$pid" 2>/dev/null; then
                log_success "Killed process $pid"
            fi
        done

        # Wait a moment for port to be released
        sleep 1
    else
        log_success "Port $port is available"
    fi
}

# Check if a port is available
is_port_available() {
    local port=$1

    if command -v lsof &>/dev/null; then
        ! lsof -ti tcp:"$port" &>/dev/null
    else
        ! netstat -vanp tcp 2>/dev/null | grep -q ".$port "
    fi
}

# Find an available port starting from the default
find_available_port() {
    local port=$DEFAULT_PORT
    local attempts=0

    while [[ $attempts -lt $MAX_PORT_ATTEMPTS ]]; do
        if is_port_available "$port"; then
            echo "$port"
            return 0
        fi

        log_warning "Port $port is in use, trying next port..."
        port=$((port + 1))
        attempts=$((attempts + 1))
    done

    log_error "Could not find an available port after $MAX_PORT_ATTEMPTS attempts"
    return 1
}

# Cleanup function to run on exit
cleanup() {
    log_info "Shutting down web server..."
}

# Open browser (macOS-aware)
open_browser() {
    local url=$1

    if [[ "$AUTO_OPEN_BROWSER" != "true" ]]; then
        return 0
    fi

    # Wait a moment for server to be ready
    sleep 2

    if command -v open &>/dev/null; then
        # macOS
        open "$url" 2>/dev/null &
    elif command -v xdg-open &>/dev/null; then
        # Linux
        xdg-open "$url" 2>/dev/null &
    elif command -v start &>/dev/null; then
        # Windows (Git Bash)
        start "$url" 2>/dev/null &
    else
        log_warning "Could not auto-open browser. Please visit: $url"
    fi
}

# Ensure dependencies are installed
ensure_setup() {
    if [[ ! -d "$VENV_DIR" ]]; then
        log_warning "Virtual environment not found. Running setup..."
        echo ""

        if [[ ! -f "${SCRIPT_DIR}/setup.sh" ]]; then
            log_error "setup.sh not found. Please run setup manually."
            exit 1
        fi

        # Run setup script
        "${SCRIPT_DIR}/setup.sh" --force-setup

        echo ""
        log_success "Setup complete. Continuing with web server startup..."
        echo ""
    fi

    # Verify codebase_reviewer is installed
    if ! "$VENV_DIR/bin/python" -c "import codebase_reviewer" 2>/dev/null; then
        log_error "codebase_reviewer package not installed. Please run ./setup.sh"
        exit 1
    fi
}

# ============================================================================
# Main Logic
# ============================================================================

main() {
    # Change to script directory
    cd "$SCRIPT_DIR"

    echo ""
    log_info "Codebase Reviewer - Web UI Startup"
    echo ""

    # Ensure setup is complete
    ensure_setup

    # Try to kill any stale processes on default port
    kill_port "$DEFAULT_PORT"

    # Find an available port
    local port
    if ! port=$(find_available_port); then
        exit 1
    fi

    if [[ "$port" != "$DEFAULT_PORT" ]]; then
        log_warning "Using alternate port: $port (default $DEFAULT_PORT was unavailable)"
    fi

    # Set up cleanup trap
    trap cleanup EXIT INT TERM

    echo ""
    log_success "Starting web server on port $port..."
    log_info "Access at: http://localhost:$port"
    echo ""
    log_warning "Press Ctrl+C to stop the server"
    echo ""

    # Open browser in background
    open_browser "http://localhost:$port" &

    # Run web server with the selected port
    PORT="$port" "$VENV_DIR/bin/python" -m codebase_reviewer web --port "$port"
}

# ============================================================================
# Entry Point
# ============================================================================

main "$@"

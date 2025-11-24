#!/usr/bin/env bash
#
# setup-all.sh - Complete setup for both Go and Python tools
#
# This script sets up the entire codebase-reviewer environment:
# - Go tool (legacy Phase 1 tool)
# - Python tool (primary comprehensive analyzer)
#
# Usage:
#   ./setup-all.sh              # Setup both tools
#   ./setup-all.sh --python-only  # Setup only Python
#   ./setup-all.sh --go-only      # Setup only Go
#   ./setup-all.sh -h           # Show help

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
PYTHON_MIN_VERSION="3.9"
GO_MIN_VERSION="1.21"

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

show_help() {
    cat <<EOF
setup-all.sh - Complete Setup for Codebase Reviewer

USAGE:
    $(basename "$0") [OPTIONS]

OPTIONS:
    -h, --help          Show this help message and exit
    --python-only       Setup only Python tool
    --go-only           Setup only Go tool
    -f, --force         Force recreation of environments
    -v, --verbose       Enable verbose output

DESCRIPTION:
    Sets up both the Go-based legacy tool and Python-based primary tool.
    By default, sets up both tools for maximum compatibility.

EXAMPLES:
    # Setup everything
    ./setup-all.sh

    # Setup only Python (recommended for most users)
    ./setup-all.sh --python-only

    # Force rebuild
    ./setup-all.sh --force

EOF
}

# ============================================================================
# Python Setup
# ============================================================================

setup_python() {
    log_info "Setting up Python environment..."

    # Find Python
    local python_cmd=""
    for cmd in python3.12 python3.11 python3.10 python3.9 python3 python; do
        if command -v "$cmd" &>/dev/null; then
            local version
            version=$("$cmd" --version 2>&1 | awk '{print $2}')
            local major minor
            major=$(echo "$version" | cut -d. -f1)
            minor=$(echo "$version" | cut -d. -f2)
            if [[ "$major" -ge 3 ]] && [[ "$minor" -ge 9 ]]; then
                python_cmd="$cmd"
                break
            fi
        fi
    done

    if [[ -z "$python_cmd" ]]; then
        log_error "Python ${PYTHON_MIN_VERSION}+ is required but not found"
        return 1
    fi

    log_info "Using Python: $python_cmd ($($python_cmd --version 2>&1))"

    # Create virtual environment
    if [[ ! -d "$VENV_DIR" ]] || [[ "${FORCE_SETUP:-false}" == "true" ]]; then
        log_info "Creating virtual environment..."
        rm -rf "$VENV_DIR" 2>/dev/null || true
        "$python_cmd" -m venv "$VENV_DIR"
    fi

    # Install dependencies
    log_info "Installing Python dependencies..."
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    "$VENV_DIR/bin/python" -m pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    pip install -e ".[dev]" --quiet

    log_success "Python environment ready"
}

# ============================================================================
# Go Setup
# ============================================================================

setup_go() {
    log_info "Setting up Go environment..."

    # Check for Go
    if ! command -v go &>/dev/null; then
        log_error "Go is not installed. Please install Go ${GO_MIN_VERSION}+ from https://golang.org/dl/"
        return 1
    fi

    local go_version
    go_version=$(go version | awk '{print $3}' | sed 's/go//')
    log_info "Using Go: $go_version"

    # Download dependencies
    log_info "Downloading Go dependencies..."
    go mod download
    go mod tidy

    # Build the binary
    log_info "Building Go binary..."
    make build

    log_success "Go environment ready"
}

# ============================================================================
# Main Logic
# ============================================================================

main() {
    local setup_python=true
    local setup_go=true
    FORCE_SETUP=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            --python-only)
                setup_go=false
                shift
                ;;
            --go-only)
                setup_python=false
                shift
                ;;
            -f|--force)
                FORCE_SETUP=true
                shift
                ;;
            -v|--verbose)
                set -x
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                echo ""
                show_help
                exit 1
                ;;
        esac
    done

    cd "$SCRIPT_DIR"

    echo ""
    log_info "Codebase Reviewer - Complete Setup"
    echo ""

    local success=true

    # Setup Python
    if [[ "$setup_python" == "true" ]]; then
        if ! setup_python; then
            log_error "Python setup failed"
            success=false
        fi
        echo ""
    fi

    # Setup Go
    if [[ "$setup_go" == "true" ]]; then
        if ! setup_go; then
            log_warning "Go setup failed (optional - Python tool will still work)"
        fi
        echo ""
    fi

    if [[ "$success" == "true" ]]; then
        log_success "Setup complete!"
        echo ""
        log_info "Next steps:"
        if [[ "$setup_python" == "true" ]]; then
            echo "  - Run Python tool: review-codebase analyze /path/to/repo"
            echo "  - Start web UI: ./start-web.sh"
        fi
        if [[ "$setup_go" == "true" ]]; then
            echo "  - Run Go tool: ./bin/generate-docs /path/to/repo"
        fi
        echo "  - Run tests: make all-tests"
        echo "  - View help: make help"
    else
        log_error "Setup failed - see errors above"
        exit 1
    fi
}

# ============================================================================
# Entry Point
# ============================================================================

main "$@"


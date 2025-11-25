.PHONY: build test lint clean install help python-test python-lint python-setup all-tests all-lint

# Binary name
BINARY_NAME=generate-docs
INSTALL_PATH=/usr/local/bin

# Go parameters
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
GOGET=$(GOCMD) get
GOMOD=$(GOCMD) mod
GOLINT=golangci-lint

# Python parameters
PYTHON=python3
PIP=$(PYTHON) -m pip
PYTEST=$(PYTHON) -m pytest
VENV_DIR=.venv

# Build flags
LDFLAGS=-ldflags "-s -w"

all: all-tests build

build: ## Build the binary
	@echo "Building $(BINARY_NAME)..."
	$(GOBUILD) $(LDFLAGS) -o bin/$(BINARY_NAME) ./cmd/generate-docs
	@echo "Build complete: bin/$(BINARY_NAME)"

test: ## Run tests
	@echo "Running tests..."
	$(GOTEST) -v -race -coverprofile=coverage.out ./...
	@echo "Tests complete"

lint: ## Run linters
	@echo "Running linters..."
	$(GOLINT) run --enable-all --timeout 5m ./...
	@echo "Linting complete"

clean: ## Clean build artifacts
	@echo "Cleaning..."
	$(GOCLEAN)
	rm -rf bin/
	rm -f coverage.out
	@echo "Clean complete"

install: build ## Install binary to system
	@echo "Installing to $(INSTALL_PATH)..."
	cp bin/$(BINARY_NAME) $(INSTALL_PATH)/
	@echo "Installed: $(INSTALL_PATH)/$(BINARY_NAME)"

deps: ## Download dependencies
	@echo "Downloading dependencies..."
	$(GOMOD) download
	$(GOMOD) tidy
	@echo "Dependencies updated"

run: build ## Build and run with example
	@echo "Running example..."
	./bin/$(BINARY_NAME) -v /Users/matt/GitHub/CallBox

help: ## Show this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# ============================================================================
# Python Tool Targets
# ============================================================================

python-setup: ## Setup Python virtual environment and install dependencies
	@echo "Setting up Python environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@. $(VENV_DIR)/bin/activate && \
		$(PIP) install --upgrade pip && \
		$(PIP) install -r requirements.txt && \
		$(PIP) install -e ".[dev]"
	@echo "Python setup complete"

python-test: ## Run Python tests with coverage
	@echo "Running Python tests..."
	@. $(VENV_DIR)/bin/activate && \
		$(PYTEST) tests/ -v --cov=src/codebase_reviewer --cov-report=xml --cov-report=term-missing --cov-fail-under=54
	@echo "Python tests complete"

python-lint: ## Run Python linters (black, isort, pylint, mypy)
	@echo "Running Python linters..."
	@. $(VENV_DIR)/bin/activate && \
		black --check --line-length=120 src/codebase_reviewer tests/ && \
		isort --check-only --profile black --line-length 120 src/codebase_reviewer tests/ && \
		pylint src/codebase_reviewer --max-line-length=120 --min-similarity-lines=10 --fail-under=9.5 && \
		mypy src/codebase_reviewer --ignore-missing-imports
	@echo "Python linting complete"

python-format: ## Auto-format Python code
	@echo "Formatting Python code..."
	@. $(VENV_DIR)/bin/activate && \
		black --line-length=120 src/codebase_reviewer tests/ && \
		isort --profile black --line-length 120 src/codebase_reviewer tests/
	@echo "Formatting complete"

python-clean: ## Clean Python artifacts
	@echo "Cleaning Python artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf htmlcov/ .coverage coverage.xml .pytest_cache/
	@echo "Python clean complete"

# ============================================================================
# Combined Targets
# ============================================================================

all-tests: test python-test ## Run both Go and Python tests

all-lint: lint python-lint ## Run both Go and Python linters

all-clean: clean python-clean ## Clean both Go and Python artifacts

setup: deps python-setup ## Setup both Go and Python environments

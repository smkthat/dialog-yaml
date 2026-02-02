.PHONY: help format check lint check-all test test-unit test-integration test-functional test-cov test-html mega-bot build dist upload-pypi upload-testpypi clean

# Detect OS
UNAME_S := $(shell uname -s)

# Metadata
PROJECT_NAME ?= $(shell sed -n 's/^name[[:space:]]*=[[:space:]]*"\(.*\)"/\1/p' pyproject.toml | head -n1)
PROJECT_VERSION ?= $(shell sed -n 's/^version[[:space:]]*=[[:space:]]*"\(.*\)"/\1/p' pyproject.toml | head -n1)
GIT_TAG ?= $(PROJECT_VERSION)

# ANSI Color Codes
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color
LINE = "$(GREEN)$(shell printf '%.0s-' {1..78})$(NC)"

# Paths
CWD_ABSOLUTE := $(shell pwd)
SRC = src
TESTS_SRC = tests
CHECK_SRC = $(SRC) $(TESTS_SRC)

# Category: Helpers

help: ## 💡 Show this help message
	@echo $(LINE)
	@printf "$(GREEN)%-23s$(NC) %s\n" "Project" "$(PROJECT_NAME)"
	@printf "$(GREEN)%-23s$(NC) %s\n" "Version" "$(PROJECT_VERSION)"
	@echo
	@echo "$(GREEN)Usage:$(NC) make $(YELLOW)<target>$(NC)"
	@echo $(LINE)
	@awk 'BEGIN {FS = ":.*?## "} \
		/^# Category:/ {printf "\n$(GREEN)  %s ↴$(NC)\n%s\n", substr($$0, 13), $(LINE)} \
		/^[a-zA-Z0-9_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo

version: ## 🔎 Show project name and version (alias v)
	@echo "Project: $(PROJECT_NAME)"
	@echo "Version: $(PROJECT_VERSION)"

v: version

lock: ## 📦 Locking dependencies
	@echo "📦 Locking dependencies..."
	uv lock

clean: ## 🧹 Clean build artifacts & cache
	@echo "🧹 Cleaning build artifacts & cache..."
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf dist/ build/ .coverage htmlcov/ .pytest_cache/ .ruff_cache/
	@echo "✅ Build artifacts & cache cleaned up!"

# Category: Code quality

format: ## 💅 Format code with Ruff
	@echo "💅 Formatting code with Ruff..."
	uv run ruff format $(CHECK_SRC)

check: format ## 🔍 Run code quality checks with Ruff
	@echo "🔍 Linting code with Ruff..."
	uv run ruff check $(CHECK_SRC) --fix
	@echo

lint: ## 🔍 Run code quality checks with Ty
	@echo "🔍 Running deep code analysis with ty..."
	uv run ty check
	@echo

check-all: check lint ## 🧠 Run format & all code quality checks
	@echo "✅ Code quality checks passed!"
	@echo

# Category: Tests

test: ## 🧪 Run all tests
	@echo "🧪 Running all tests..."
	uv run pytest -v --no-header -x $(PYTEST_ADDOPTS)

test-unit: ## 🧪 Run unit tests
	@echo "🧪 Running unit tests..."
	uv run pytest $(TESTS_SRC)/unit -v --no-header -x $(PYTEST_ADDOPTS)

test-integration: ## 🧪 Run integration tests
	@echo "🧪 Running integration tests..."
	uv run pytest $(TESTS_SRC)/integration -v --no-header -x $(PYTEST_ADDOPTS)

test-functional: ## 🧪 Run functional tests
	@echo "🧪 Running functional tests..."
	uv run pytest $(TESTS_SRC)/functional -v --no-header -x $(PYTEST_ADDOPTS)

test-cov: ## 📊 Generating test coverage report
	@echo "📊 Generating test coverage report..."
	uv run pytest -v --no-header --cov=$(SRC) $(PYTEST_ADDOPTS)

test-html: ## 📊 Generating HTML test coverage report
	@echo "📊 Generating HTML test coverage report..."
	uv run pytest -v --no-header --cov=$(SRC) --cov-report=html $(PYTEST_ADDOPTS)
	@echo
	@echo "📄 See coverage report in htmlcov/index.html"

# Category: Publish

build: clean ## 📦 Build package distributions
	@echo "📦 Building package distributions..."
	uv run python -m build
	@echo "✅ Package distributions built successfully!"
	@echo "📦 Files created:"
	@ls -la dist/

upload-pypi: ## 🚀 Upload package to PyPI
	@echo "🚀 Uploading package to PyPI..."
	uv run python -m twine upload dist/*

upload-testpypi: ## 🧪 Upload package to TestPyPI
	@echo "🧪 Uploading package to TestPyPI..."
	uv run python -m twine upload --repository testpypi dist/*

dist: ## 📦 Show distribution files
	@echo "📦 Distribution files:"
	@ls -la dist/
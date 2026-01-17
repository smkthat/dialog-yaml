.PHONY: help format check lint check-all test test-cov test-html

# Detect OS
UNAME_S := $(shell uname -s)

# ANSI Color Codes
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

CWD := $(shell pwd)
MAIN_MODULE = src
CHECK_SRC = src

help: # 💡 Show this help message
	@echo "$(GREEN)spoetka-base$(NC)"
	@echo "-------------------------------------"
	@echo "Usage: make $(YELLOW)<target>$(NC)"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?# "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  $(YELLOW)%-18s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

format: ## 🧠 Format code with Ruff
	@echo "🔧 Formatting code with Ruff..."
	uv run ruff format $(CHECK_SRC)

check: ## 🧠 Run code quality checks with Ruff
	@echo "🔍 Linting code with Ruff..."
	uv run ruff check $(CHECK_SRC) --fix
	uv run ty check
	@echo

lint: ## 🧠 Run code quality checks with Pylint
	@echo "🧠 Running deep code analysis with Pylint..."
	uv run pylint $(CHECK_SRC)

check-all: format check lint ## 🧠 Run format & all code quality checks
	@echo "✅ Code quality checks passed!"
	@echo

test: ## 🧪 Run tests
	@echo "🧪 Running tests..."
	uv run pytest -v --no-header

test-cov: ## 📊 Generating test coverage report
	@echo "📊 Generating test coverage report..."
	uv run pytest -v --no-header --cov

test-html: ## 📊 Generating HTML test coverage report
	@echo "📊 Generating HTML test coverage report..."
	uv run pytest -v --no-header --cov --cov-report=html
	@echo
	@echo "📄 See coverage report in htmlcov/index.html"
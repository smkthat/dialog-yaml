.PHONY: help format check lint check-all test test-cov test-html mega-bot build dist upload-pypi upload-testpypi clean

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

mega-bot: ## 🤖 Run mega bot example (requires cloning examples repo)
	@echo "🤖 Running mega bot example..."
	@if [ ! -d "dialog-yml-examples" ]; then \
		echo "⚠️  Warning: dialog-yml-examples directory not found"; \
		echo "Please clone the examples repository first:"; \
		echo "git clone https://github.com/smkthat/dialog-yml-examples.git"; \
		exit 1; \
	fi
	cd dialog-yml-examples/mega && PYTHONPATH=. uv run bot.py

build: clean ## 📦 Build package distributions
	@echo "📦 Building package distributions..."
	uv run python -m build
	@echo "✅ Package distributions built successfully!"
	@echo "📦 Files created:"
	@ls -la dist/

dist: ## 📦 Show distribution files
	@echo "📦 Distribution files:"
	@ls -la dist/

upload-pypi: ## 🚀 Upload package to PyPI
	@echo "🚀 Uploading package to PyPI..."
	uv run python -m twine upload dist/*

upload-testpypi: ## 🧪 Upload package to TestPyPI
	@echo "🧪 Uploading package to TestPyPI..."
	uv run python -m twine upload --repository testpypi dist/*

clean: ## 🧹 Clean build artifacts & cache
	@echo "🧹 Cleaning build artifacts & cache..."
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf dist/ build/ .coverage htmlcov/ .pytest_cache/ .ruff_cache/
	@echo "✅ Build artifacts & cache cleaned up!"
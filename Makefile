.PHONY: test test-verbose install help

# Default target
.DEFAULT_GOAL := help

## help: Display this help message
help:
	@echo "Available commands:"
	@echo "  make test          - Run all test cases across all subprojects"
	@echo "  make test-verbose  - Run all test cases with verbose output"
	@echo "  make install       - Install Playwright browser dependencies"

## test: Run all test cases across all subprojects
test:
	uv run pytest

## test-verbose: Run all test cases with verbose output (-v)
test-verbose:
	uv run pytest -v

## install: Install Playwright browser runtimes
install:
	uv run playwright install

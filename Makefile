# Display this help message
.PHONY: help
help:
	@awk '/^.PHONY:/ && (a ~ /#/) {gsub(/.PHONY: /, "", $$0); gsub(/# /, "", a); printf "%s @ %s\n", $$0, a}{a=$$0}' $(MAKEFILE_LIST) | column -s "@" -t

# Set up for development
.PHONY: setup
setup:
	@./scripts/setup.sh

# Format Lua source
.PHONY: fmt-lua
fmt-lua:
	@lua-format -i lua/*

# Format Python source
.PHONY: fmt-python
fmt-python:
	@poetry run sh -c "isort . && black ."

# Format Shell source
.PHONY: fmt-shell
fmt-shell:
	@shfmt -i 2 -w scripts/

# Format all source
.PHONY: fmt
fmt: fmt-lua fmt-python fmt-shell

# Lint & check Python source
.PHONY: lint-python
lint-python:
	@poetry run sh -c "autoflake -ir --remove-all-unused-imports --remove-unused-variables . && mypy ."

# Format & lint all source
.PHONY: lint
lint: fmt lint-python

# Run Python unit tests
.PHONY: test-python
test-python:
	@poetry run python -m unittest

# Run all unit tests
.PHONY: test
test: test-python

# Run ConfGen - generates NGINX config files from sources
.PHONY: confgen
confgen:
	@poetry run python -m confgen

# Build the Docker entrypoint Golang binary
.PHONY: entrypoint
entrypoint:
	@go build -o docker-entrypoint ./entrypoint
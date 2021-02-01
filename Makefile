# Display this help message
.PHONY: help
help:
	@awk '/^.PHONY:/ && (a ~ /#/) {gsub(/.PHONY: /, "", $$0); gsub(/# /, "", a); printf "%s @ %s\n", $$0, a}{a=$$0}' $(MAKEFILE_LIST) | column -s "@" -t

# Set up for development
.PHONY: setup
setup:
	@./scripts/dev.sh

# Format Shell source
.PHONY: fmt-shell
fmt-shell:
	@shfmt -i 2 -w scripts/

# Format all source
.PHONY: fmt
fmt: fmt-shell

# Lint & check Python source
.PHONY: lint-python
lint-python: fmt
	@poetry run lint

# Format & lint all source
.PHONY: lint
lint: fmt lint-python

# Run Python unit tests
.PHONY: test-python
test-python:
	@poetry run python -m unittest --verbose

# Run all unit tests
.PHONY: test
test: test-python

all: help

.PHONY: install
install: ## Install dependencies
	@echo "Installing dependencies..."
	@poetry install

.PHONY: format
format: ## Run ruff formatter
	 @echo "Running ruff formatter..."
	 @poetry run ruff format .

.PHONY: lint
lint: ## Run ruff linter
	 @echo "Running ruff linter..."
	 @poetry run ruff check . --fix

.PHONY: run
run: ## Run the application
	@echo "Running the application..."
	@poetry run python main.py

.PHONY: test
test: ## Run tests
	@echo "Running tests..."
	@poetry run coverage run -m pytest tests/

.PHONY: coverage
coverage: ## Show code coverage
	@echo "Show code coverage ..."
	@poetry run coverage report -m

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

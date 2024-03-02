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
	@poetry run pytest tests/

.PHONY: coverage
coverage: ## Build coverage files
	@echo "Build coverage files..."
	@poetry run pytest --junitxml=coverage.xml --cov-report=term-missing:skip-covered --cov=main --cov=gross_net_calculator tests/ | tee coverage.txt

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

SHELL=/bin/bash

.DEFAULT_GOAL := help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


install: ## Install packages for all services
	uv sync --frozen --no-cache

run: ## Run the application
	docker compose up --build -d
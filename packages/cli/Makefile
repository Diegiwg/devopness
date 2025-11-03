IMAGE ?= devopness-cli
TAG ?= latest

PWD := $(shell pwd)
USER_ID := $(shell id -u)
GROUP_ID := $(shell id -g)

WORKDIR := cli

.DEFAULT_GOAL := help
.PHONY: build-image shell build-cli publish lint format test-unit help

##@ Docker

build-image: ## 🔧 Build the Docker image (optional: PYTHON_VERSION / ALPINE_VERSION)
	$(info 🐳 Building Docker image...)
	@docker build \
		-f Dockerfile \
		$(if $(PYTHON_VERSION),--build-arg PYTHON_VERSION=$(PYTHON_VERSION),) \
		$(if $(ALPINE_VERSION),--build-arg ALPINE_VERSION=$(ALPINE_VERSION),) \
		-t $(IMAGE):$(TAG) .

shell: build-image ## 🐚 Open a shell inside the CLI container
	$(info 🔧 Starting interactive shell in CLI container...)
	@docker run --rm -it \
		-v $(PWD):/$(WORKDIR) \
		--name devopness-cli-shell \
		$(IMAGE):$(TAG) \
		/bin/bash

##@ CLI Build & Publish

build-cli: build-image ## ⚙️  Build the Devopness CLI for Python
	$(info 🏗️  Building CLI using Docker...)
	@docker run --rm \
		-u $(USER_ID):$(GROUP_ID) \
		-v $(PWD):/$(WORKDIR) \
		--name devopness-cli-build \
		$(IMAGE):$(TAG) \
		/bin/bash -ce ' \
			GENERATED_FILES=src/devopness/generated; \
			CLI_MODELS_FILE=src/devopness/models.py; \
			FILES_TO_FORMAT="$$GENERATED_FILES $$CLI_MODELS_FILE"; \
			\
			scripts/build.py; \
			\
			echo "🔧  Formatting generated files..."; \
			ruff check --fix --select I  -s $$FILES_TO_FORMAT; \
			ruff check --fix --exit-zero -s $$FILES_TO_FORMAT; \
			ruff format                  -s $$FILES_TO_FORMAT; \
			\
			echo "✅  Devopness CLI - Python Build Completed"; \
		'

publish: build-image ## 🚀 Publish the CLI to PyPI (requires PYPI_TOKEN)
	$(info 📦 Publishing CLI to PyPI...)
	@docker run --rm \
		-v $(PWD):/$(WORKDIR) \
		--env DEVOPNESS_CLI_PYTHON_PYPI_TOKEN=$(PYPI_TOKEN) \
		--name devopness-cli-publish \
		$(IMAGE):$(TAG) \
		/bin/bash -cex ' \
			poetry config pypi-token.pypi "$$DEVOPNESS_CLI_PYTHON_PYPI_TOKEN" &> /dev/null; \
			poetry publish --build; \
		'

##@ Lint & Format

lint: build-image ## 🔍 Run linting tools (ruff, mypy)
	$(info 🧹 Running linters...)
	@docker run --rm \
		-v $(PWD):/$(WORKDIR) \
		--name devopness-cli-lint \
		$(IMAGE):$(TAG) \
		/bin/bash -cex ' \
			poetry run ruff check . && \
			poetry run ruff format . --check && \
			poetry run mypy --enable-error-code exhaustive-match . \
		'

format: build-image ## 🧼 Auto-format code with ruff
	$(info ✨ Formatting code...)
	@docker run --rm \
		-v $(PWD):/$(WORKDIR) \
		--name devopness-cli-format \
		$(IMAGE):$(TAG) \
		/bin/bash -cex ' \
			poetry run ruff check --fix && \
			poetry run ruff format . \
		'

##@ Tests

test-unit: build-image ## 🧪 Run unit tests
	$(info 🧪 Running unit tests...)
	@docker run --rm \
		-v $(PWD):/$(WORKDIR) \
		--name devopness-cli-tests \
		$(IMAGE):$(TAG) \
		/bin/bash scripts/test-unit.sh

##@ Utilities

help: ## 📖 Show this help message
# `help` function obtained from https://gist.github.com/prwhite/8168133#gistcomment-4160123
	@echo "Devopness CLI - Python"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} \
	/^[a-zA-Z0-9_-]+:.*##/ { \
		printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 \
	}' $(MAKEFILE_LIST)

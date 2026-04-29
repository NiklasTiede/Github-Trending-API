
# ------------- Run with Uvicorn ------------------------------

.PHONY: run

run: ## run App on uvicorn server
	python -m uvicorn app.main:app --host 127.0.0.1 --port 1313 --reload



# ------------- Test/Lint  ------------------------------------

.PHONY: sync pre-commit pre-commit-update lint lint-fix test

sync: ## install project and development dependencies with uv
	uv sync --dev

pre-commit:
	uv run pre-commit run --all-files

pre-commit-update:
	uv run pre-commit autoupdate

lint: ## check style with Ruff
	uv run ruff check app tests

lint-fix: ## fix lint issues with Ruff
	uv run ruff check --fix app tests

test: ## run tests quickly with the default Python
	uv run pytest -v



# ------------- Clean Test/Lint Artifacts  ---------------------

.PHONY: clean clean-pyc clean-test

clean: clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .mypy_cache
	rm -fr .pytest_cache



# ------------  Docker  -----------------------------------

.PHONY: docker-build docker-run docker-clean

DOCKER_IMAGE = github-trending-api

docker-build: ## build docker image from Dockerfile
	docker build -t $(DOCKER_IMAGE) .

docker-run: ## run API docker container
	docker run -p 5000:5000 $(DOCKER_IMAGE)

docker-clean: ## remove docker image
	docker rmi -f $(DOCKER_IMAGE)



# ------------  Help  --------------------------------------

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

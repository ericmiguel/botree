dir     = $(shell pwd)
root    = $(shell dirname $(dir))
project = $(shell basename $(dir))

python/install:
	@echo "INFO: creating venv '$(dir)'"
	@poetry config --local virtualenvs.in-project true
	@poetry install

python/activate:
	@echo execute: 'source $(shell poetry env info --path)/bin/activate'

python/format:
	@echo "INFO: running Black..."
	@black botree tests

	@echo "INFO: running Isort..."
	@isort botree tests

python/lint:
	@echo "INFO: running Autoflake8..."
	@autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place botree tests --exclude=__init__.py

	@echo "INFO: running Pydocstyle.."
	@pydocstyle botree

	@echo "INFO: running mypy..."
	@mypy botree

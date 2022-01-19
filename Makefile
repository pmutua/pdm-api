SHELL := /bin/bash

MAKEFLAGS     = --no-print-directory --no-builtin-rules
.DEFAULT_GOAL = all

# Variables
PACKAGE = pdm

# If virtualenv exists, use it. If not, use PATH to find
SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
PYTHON         = $(or $(wildcard venv/bin/python), $(SYSTEM_PYTHON))

all: test build


.PHONY: all



venv: ## Create Environment with name venv
	rm -rf venv
	$(SYSTEM_PYTHON) -m venv venv


deps: ## Install Dependencies
	$(PYTHON) -m pip install --upgrade pip -r requirements/base.txt -r requirements/local.txt


.PHONY: venv deps


test: ## Lint, test
	$(PYTHON) -m tox


dev/test: ## Run tests in development mode
	$(PYTHON) -m tox -e py39


dev/lint: ## Lint
	$(PYTHON) -m tox -e lint


.PHONY: install


run: ## Run the application
	python manage.py runserver


clean: ## Clean project files
	rm -rf .out .pytest_cache .tox *.egg-info dist build

.PHONY: clean


migration: ## Create database migrations
	python manage.py makemigrations


migrate: ## Apply database migrations
	python manage.py migrate


superuser: ## Create Super User
	python manage.py createsuperuser


help: ## Help Commands           
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


# deploy:

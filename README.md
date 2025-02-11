# Django Meilisearch

A Meilisearch integration for Django project

[![Documentation](https://img.shields.io/badge/Documentação-Acessar-blue)](https://lucashcr.github.io/django_meilisearch/)

[![PyPI version](https://badge.fury.io/py/django-meilisearch.svg)](https://badge.fury.io/py/django-meilisearch)

![workflow](https://github.com/Lucashcr/django_meilisearch/actions/workflows/main.yaml/badge.svg)

## How to run

Start a Docker container with Meilisearch:

> docker run --rm -p 7700:7700 getmeili/meilisearch:latest

Init a python virtual environment:

> poetry install

ou

> python3 -m venv venv

Run the Django development server

> task serve

## Initial tasks

- [x] Implements documents class
- [x] Implements search method
- [x] Implements commands (create_index, delete_index, populate, rebuild, ...)
- [x] Refactor DocType and Document classes to separated files
- [x] Create django signals to add, update or remove data from index
- [x] Create search method that returns queryset
- [x] Create a progress viewer while indexing data
- [x] Config Mypy type checking and solve errors
- [x] Config Black code format and apply it
- [x] Solve Pylint advices
- [x] Review tests coverage
- [x] Implements GitHub Actions workflow

# Django Meilisearch

A Meilisearch integration for Django project

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
- [ ] Refactor DocType and Document classes to separated files
- [ ] Refactor search method to return only results (returns TypedDict)
- [ ] Create search method that returns queryset
- [ ] Implements views (explore indexed data) ???

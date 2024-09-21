"""
# Django MeiliSearch

This library provides a simple way to integrate MeiliSearch with Django.
It allows you to define indexes for your Django models and provides methods
to interact with MeiliSearch. It also provides a management command to
perform actions on the indexes.
"""

from django.conf import settings

from meilisearch.client import Client as MeiliClient


client = MeiliClient(**settings.DJANGO_MEILISEARCH)

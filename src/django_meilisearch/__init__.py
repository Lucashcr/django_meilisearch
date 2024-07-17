from django.utils.module_loading import autodiscover_modules
from django.conf import settings

from meilisearch.client import Client as MeiliClient


client = MeiliClient(**settings.DJANGO_MEILISEARCH)


def autodiscover():
    autodiscover_modules("documents")

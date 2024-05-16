from django.utils.module_loading import autodiscover_modules
from django.conf import settings

from meilisearchdsl import MeiliClient


client = MeiliClient(**settings.DJANGO_MEILISEARCH)


def autodiscover():
    autodiscover_modules("documents")

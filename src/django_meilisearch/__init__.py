from django.utils.module_loading import autodiscover_modules
from django.conf import settings

from meilisearchdsl import Client


client = Client(**settings.DJANGO_MEILISEARCH)

def autodiscover():
    autodiscover_modules("documents")
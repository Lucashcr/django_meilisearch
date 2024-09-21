"""
App configuration for the django_meilisearch app.
"""

from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class DjangoMeilisearchConfig(AppConfig):
    """
    App configuration for the django_meilisearch app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_meilisearch"

    def ready(self):
        autodiscover_modules("indexes")

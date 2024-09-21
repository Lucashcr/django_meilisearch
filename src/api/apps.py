"""
App configuration for the api app.
"""

from django.apps import AppConfig


class ApiTestConfig(AppConfig):
    """
    App configuration for the api app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

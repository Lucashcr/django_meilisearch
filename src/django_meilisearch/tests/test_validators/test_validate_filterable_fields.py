from django.db import models
from django.test import TestCase

from django_meilisearch.validators import validate_filterable_fields
from django_meilisearch.exceptions import InvalidFilterableFieldError


class TestValidateFilterableFields(TestCase):
    @classmethod
    def setUpTestData(cls):
        class FilterableFieldsPostModel(models.Model):
            title = models.CharField(max_length=100)
            content = models.TextField()
            created_at = models.DateTimeField(auto_now_add=True)

        cls.model = FilterableFieldsPostModel

    def test_non_list_filterable_fields_argument(self):
        with self.assertRaises(InvalidFilterableFieldError):
            validate_filterable_fields(self.model, "invalid_filterable_fields")

    def test_existing_filterable_fields(self):
        filterable_fields = ["title", "content", "created_at"]

        validate_filterable_fields(self.model, filterable_fields)

    def test_non_existing_filterable_fields(self):
        filterable_fields = ["title", "content", "created_at", "invalid_field"]

        with self.assertRaises(InvalidFilterableFieldError):
            validate_filterable_fields(self.model, filterable_fields)

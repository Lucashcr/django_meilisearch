from django.db import models
from django.test import TestCase

from django_meilisearch.validators import validate_searchable_fields
from django_meilisearch.exceptions import InvalidSearchableFieldError


class TestValidateSearchableFields(TestCase):
    @classmethod
    def setUpTestData(cls):
        class SearchableFieldsPostModel(models.Model):
            title = models.CharField(max_length=100)
            content = models.TextField()
            created_at = models.DateTimeField(auto_now_add=True)

        cls.model = SearchableFieldsPostModel

    def test_non_list_searchable_fields_argument(self):
        with self.assertRaises(InvalidSearchableFieldError):
            validate_searchable_fields(self.model, "invalid_searchable_fields")

    def test_existing_searchable_fields(self):
        searchable_fields = ["title", "content", "created_at"]

        validate_searchable_fields(self.model, searchable_fields)

    def test_non_existing_searchable_fields(self):
        searchable_fields = ["title", "content", "created_at", "invalid_field"]

        with self.assertRaises(InvalidSearchableFieldError):
            validate_searchable_fields(self.model, searchable_fields)

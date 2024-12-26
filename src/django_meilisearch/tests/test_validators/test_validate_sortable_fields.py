from django.db import models
from django.test import TestCase

from django_meilisearch.validators import validate_sortable_fields
from django_meilisearch.exceptions import InvalidSortableFieldError


class TestValidateSortableFields(TestCase):
    @classmethod
    def setUpTestData(cls):
        class SortableFieldsPostModel(models.Model):
            title = models.CharField(max_length=100)
            content = models.TextField()
            created_at = models.DateTimeField(auto_now_add=True)

        cls.model = SortableFieldsPostModel

    def test_non_list_sortable_fields_argument(self):
        with self.assertRaises(InvalidSortableFieldError):
            validate_sortable_fields(self.model, "invalid_sortable_fields")

    def test_existing_sortable_fields(self):
        sortable_fields = ["title", "content", "created_at"]

        validate_sortable_fields(self.model, sortable_fields)

    def test_non_existing_sortable_fields(self):
        sortable_fields = ["title", "content", "created_at", "invalid_field"]

        with self.assertRaises(InvalidSortableFieldError):
            validate_sortable_fields(self.model, sortable_fields)

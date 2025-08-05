from pyexpat import model
from django.test import TestCase

from django_meilisearch.utils import get_datetime_fields
from example.models import Post


class GetDatetimeFieldsTestCase(TestCase):
    """
    Test case for the get_datetime_fields function.
    """

    def test_get_datetime_fields(self):
        """
        Test that the get_datetime_fields function returns the correct datetime fields.
        """
        datetime_fields = get_datetime_fields(Post)
        expected_fields = {"created_at"}
        self.assertEqual(set(datetime_fields), expected_fields)

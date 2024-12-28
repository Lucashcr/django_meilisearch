from datetime import datetime

from django.test import TestCase

from django_meilisearch.serializers import TimestampField
from django.utils.timezone import get_current_timezone


class TestTimestampField(TestCase):
    def setUp(self):
        self.serializer_field = TimestampField()

    def test_to_representation(self):
        value = datetime(2024, 12, 26, 22, 50)
        representation = self.serializer_field.to_representation(value)
        result = 1735253400.0
        self.assertEqual(representation, result)
        

    def test_to_internal_value(self):
        value = 1735253400.0
        internal_value = self.serializer_field.to_internal_value(value)
        result = datetime(2024, 12, 26, 22, 50, tzinfo=get_current_timezone())
        self.assertEqual(internal_value, result)

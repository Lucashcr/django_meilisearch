from django.test import TestCase
from rest_framework.serializers import ModelSerializer

from django_meilisearch.validators import validate_drf_serializer
from example.serializers import PostSerializerWithTimestamp


class ValidateDRFSerializerTestCase(TestCase):
    """
    Test case for the validate_drf_serializer function.
    """

    def test_valid_serializer_class(self):
        """
        Test that an invalid serializer class raises a TypeError.
        """

        class ValidSerializer(ModelSerializer): ...

        validate_drf_serializer("IndexWithValidSerializer", ValidSerializer)

    def test_invalid_serializer_class(self):
        """
        Test that an invalid serializer class raises a TypeError.
        """

        class InvalidSerializer: ...

        with self.assertRaises(TypeError):
            validate_drf_serializer(
                "IndexWithInvalidSerializer", InvalidSerializer
            )

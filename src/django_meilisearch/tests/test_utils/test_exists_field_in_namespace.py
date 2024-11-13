"""
Test cases for the exists_field_in_namespace function.
"""

from django.test import TestCase

from django_meilisearch.utils import exists_field_in_namespace


class ExistsFieldInNamespaceTestCase(TestCase):
    """
    Test cases for the exists_field_in_namespace function.
    """

    def test_should_return_true_for_existing_field(self):
        """
        Test the function returns True for an existing field.
        """
        namespace = {"valid_field": "Test value"}

        result = exists_field_in_namespace("valid_field", namespace)

        self.assertTrue(result)

    def test_should_return_true_for_existing_field_with_a_child(self):
        """
        Test the function returns True for an existing field with a child.
        """

        # pylint: disable=missing-class-docstring
        # pylint: disable=too-few-public-methods
        class Index:
            valid_field = "Test value"

        namespace = {"index": Index}

        result = exists_field_in_namespace("index__valid_field", namespace)

        self.assertTrue(result)

    def test_should_return_true_for_existing_field_with_a_deep_child(self):
        """
        Test the function returns True for an existing field with deep child.
        """

        # pylint: disable=missing-class-docstring
        # pylint: disable=too-few-public-methods
        class Index:
            class Inner:
                valid_field = "Test value"

        namespace = {"index": Index}

        result = exists_field_in_namespace(
            "index__Inner__valid_field", namespace
        )

        self.assertTrue(result)

    def test_should_return_false_for_non_existing_field(self):
        """
        Test the function returns False for a non-existing field.
        """
        namespace = {"valid_field": "Test value"}

        result = exists_field_in_namespace("invalid_field", namespace)

        self.assertFalse(result)

    def test_should_return_false_for_non_existing_field_with_a_child(self):
        """
        Test the function returns False for a non-existing field with a child.
        """

        # pylint: disable=missing-class-docstring
        # pylint: disable=too-few-public-methods
        class Index:
            valid_field = "Test value"

        namespace = {"index": Index}

        result = exists_field_in_namespace("index__invalid_field", namespace)

        self.assertFalse(result)

    def test_should_return_false_for_non_existing_field_with_a_deep_children(
        self,
    ):
        """
        Test the function returns False for a non-existing field with deep children.
        """

        # pylint: disable=missing-class-docstring
        # pylint: disable=too-few-public-methods
        class Index:
            class Inner:
                valid_field = "Test value"

        namespace = {"field": Index}

        result = exists_field_in_namespace(
            "index__Inner__invalid_field", namespace
        )

        self.assertFalse(result)

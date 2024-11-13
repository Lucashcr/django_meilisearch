"""
Test cases for the instantiation of the index.
"""

from django.db.models import Model, fields
from django.test import TestCase

from django_meilisearch.exceptions import (
    InvalidDjangoModelError,
    InvalidFilterableFieldError,
    InvalidIndexNameError,
    InvalidPrimaryKeyError,
    InvalidSearchableFieldError,
    InvalidSortableFieldError,
    MissingRequiredFieldError,
)
from django_meilisearch.indexes import BaseIndex


# Create your tests here.
class TestInitialize(TestCase):
    """
    Test cases for the instantiation of the index.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test cases.
        """

        class TestModel(Model):
            """
            Test model for the index.
            """

            id = fields.AutoField(primary_key=True)
            name = fields.CharField(max_length=100)
            description = fields.TextField()

        cls.model = TestModel

    def test_successful_instantiate(self):
        """
        Test the success of the instance.
        """

        class IndexCls(BaseIndex):
            """
            Test index class.
            """

            name = "test_index"
            model = self.model

        field_names = [field.name for field in self.model._meta.fields]
        index_label = BaseIndex.INDEX_NAMES[IndexCls.name]

        self.assertEqual(IndexCls.name, "test_index")
        self.assertEqual(IndexCls.model, self.model)
        self.assertEqual(IndexCls.primary_key_field, "id")
        self.assertEqual(IndexCls.searchable_fields, field_names)
        self.assertEqual(IndexCls.filterable_fields, field_names)
        self.assertEqual(IndexCls.sortable_fields, field_names)

        self.assertIn(IndexCls.name, BaseIndex.INDEX_NAMES)
        self.assertIn(index_label, BaseIndex.REGISTERED_INDEXES)

    def test_failed_instantiate_not_informed_name(self):
        """
        Test the failure of the instance when the name is not informed.
        """
        with self.assertRaises(MissingRequiredFieldError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                model = self.model

    def test_failed_instantiate_with_invalid_name(self):
        """
        Test the failure of the instance when the name is not informed.
        """
        with self.assertRaises(InvalidIndexNameError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                name = 1
                model = self.model

    def test_failed_instantiate_not_informed_model(self):
        """
        Test the failure of the instance when the model is not informed.
        """
        with self.assertRaises(MissingRequiredFieldError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                name = "test_index"

    def test_failed_instantiate_with_invalid_model(self):
        """
        Test the failure of the instance when the model is not informed.
        """

        # pylint: disable=too-few-public-methods
        class FakeModel:
            """Invalid model"""

        with self.assertRaises(InvalidDjangoModelError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                name = "test_index"
                model = FakeModel

    def test_successful_instantiate_valid_primary_key(self):
        """
        Test the failure of the instance when the primary key is not informed.
        """

        class TestIndexCls(BaseIndex):
            """
            Test index class.
            """

            name = "test_index"
            model = self.model
            primary_key_field = "id"

        self.assertEqual(TestIndexCls.name, "test_index")
        self.assertEqual(TestIndexCls.model, self.model)
        self.assertEqual(TestIndexCls.primary_key_field, "id")

    def test_failed_instantiate_invalid_primary_key(self):
        """
        Test the failure of the instance when the primary key is invalid.
        """
        with self.assertRaises(InvalidPrimaryKeyError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                name = "test_index"
                model = self.model
                primary_key_field = "invalid"

    def test_failed_instantiate_invalid_primary_key_type(self):
        """
        Test the failure of the instance when the primary key is invalid.
        """
        with self.assertRaises(InvalidPrimaryKeyError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                name = "test_index"
                model = self.model
                primary_key_field = 1

    def test_successful_instantiate_searchable_fields(self):
        """
        Test the success of the instance with searchable fields.
        """

        class TestIndexCls(BaseIndex):
            """
            Test index class.
            """

            name = "test_index"
            model = self.model
            searchable_fields = ["name"]

        self.assertEqual(TestIndexCls.name, "test_index")
        self.assertEqual(TestIndexCls.model, self.model)
        self.assertEqual(TestIndexCls.primary_key_field, "id")
        self.assertEqual(TestIndexCls.searchable_fields, ["name"])

    def test_failed_instantiate_invalid_searchable_fields(self):
        """
        Test the failure of the instance with invalid searchable fields.
        """
        with self.assertRaises(InvalidSearchableFieldError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                name = "test_index"
                model = self.model
                searchable_fields = ["invalid"]

    def test_successful_instantiate_filterable_fields(self):
        """
        Test the success of the instance with filterable fields.
        """

        class TestIndexCls(BaseIndex):
            """
            Test index class.
            """

            name = "test_index"
            model = self.model
            filterable_fields = ["name"]

        self.assertEqual(TestIndexCls.name, "test_index")
        self.assertEqual(TestIndexCls.model, self.model)
        self.assertEqual(TestIndexCls.primary_key_field, "id")
        self.assertEqual(TestIndexCls.filterable_fields, ["name"])

    def test_failed_instantiate_invalid_filterable_fields(self):
        """
        Test the failure of the instance with invalid filterable fields.
        """
        with self.assertRaises(InvalidFilterableFieldError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                name = "test_index"
                model = self.model
                filterable_fields = ["invalid"]

    def test_successful_instantiate_sortable_fields(self):
        """
        Test the success of the instance with sortable fields.
        """

        class TestIndexCls(BaseIndex):
            """
            Test index class.
            """

            name = "test_index"
            model = self.model
            sortable_fields = ["name"]

        self.assertEqual(TestIndexCls.name, "test_index")
        self.assertEqual(TestIndexCls.model, self.model)
        self.assertEqual(TestIndexCls.primary_key_field, "id")
        self.assertEqual(TestIndexCls.sortable_fields, ["name"])

    def test_failed_instantiate_invalid_sortable_fields(self):
        """
        Test the failure of the instance with invalid sortable fields.
        """
        with self.assertRaises(InvalidSortableFieldError):
            # pylint: disable=unused-variable
            class TestIndexCls(BaseIndex):
                """
                Test index class.
                """

                name = "test_index"
                model = self.model
                sortable_fields = ["invalid"]

"""
Test cases to add, update or remove single document methods.
"""

from django.test import TestCase

from example.indexes import PostIndex
from example.models import Post


class TestHandleSingleDocumentTestCase(TestCase):
    """Test cases to add, update or remove single document methods."""

    @classmethod
    def setUpClass(cls):
        """Set up the test cases."""
        PostIndex.create()

    def test_add_single_document(self):
        """Test add single document."""
        post = Post.objects.create(
            title="Test Post",
            content="This is a test post",
        )

        task = PostIndex.add_single_document(post)
        self.assertEqual(task.status, "succeeded")
        self.assertEqual(task.type, "documentAdditionOrUpdate")

        # pylint: disable=unsubscriptable-object
        self.assertEqual(task.details["receivedDocuments"], 1)

        # pylint: disable=unsubscriptable-object
        self.assertEqual(task.details["indexedDocuments"], 1)

    def test_remove_single_document(self):
        """Test remove single document."""
        post = Post.objects.create(
            title="Test Post",
            content="This is a test post",
        )

        task = PostIndex.add_single_document(post)
        self.assertEqual(task.status, "succeeded")
        self.assertEqual(task.type, "documentAdditionOrUpdate")

        # pylint: disable=unsubscriptable-object
        self.assertEqual(task.details["receivedDocuments"], 1)

        # pylint: disable=unsubscriptable-object
        self.assertEqual(task.details["indexedDocuments"], 1)

        task = PostIndex.remove_single_document(post)
        print(task)
        self.assertEqual(task.status, "succeeded")
        self.assertEqual(task.type, "documentDeletion")

        # pylint: disable=unsubscriptable-object
        self.assertEqual(task.details["providedIds"], 1)

        # pylint: disable=unsubscriptable-object
        self.assertEqual(task.details["deletedDocuments"], 1)

    @classmethod
    def tearDownClass(cls):
        PostIndex.destroy()

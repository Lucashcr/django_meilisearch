"""
Test cases for the instantiation of the index.
"""

from django.test import TestCase

from example.indexes import PostIndex, PostIndexWith10IndexingBatchSize


# Create your tests here.
class TestIndexingBatchSizeFlag(TestCase):
    """
    Test cases for the instantiation of the index.
    """

    fixtures = ["posts.json"]
    
    def test_default_indexing_batch_size_flag(self):
        """
        Test the success of the instance.
        """

        self.assertEqual(PostIndex.indexing_batch_size, 100_000)

    def test_indexing_batch_size_flag_as_default(self):
        """
        Test the success of the instance.
        """

        PostIndex.create()
        tasks = PostIndex.populate()
        PostIndex.clean()
        PostIndex.destroy()

        self.assertEqual(len(tasks), 1)

    def test_indexing_batch_size_flag_as_10(self):
        """
        Test the success of the instance.
        """

        PostIndexWith10IndexingBatchSize.create()
        tasks = PostIndexWith10IndexingBatchSize.populate()
        PostIndexWith10IndexingBatchSize.clean()
        PostIndexWith10IndexingBatchSize.destroy()

        self.assertEqual(len(tasks), 5)

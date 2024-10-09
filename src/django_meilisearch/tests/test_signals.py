"""
"""

import time
from django.test import TestCase

from api.models import Post
from api.indexes import PostIndex


class TestMeilisearchSignals(TestCase):
    """
    Test cases for the Meilisearch signals.
    It's responsible for testing the signals
    that are triggered when a model is created,
    updated or deleted.
    """

    def test_add_single_document(self):
        """
        Test the addition of a single document.
        """
        count_before = PostIndex.count()
        Post.objects.create(title="test", content="test")
        time.sleep(1)
        count_after = PostIndex.count()

        self.assertEqual(count_after, count_before + 1)

    def test_remove_single_document(self):
        """
        Test the removal of a single document.
        """
        post = Post.objects.create(title="test", content="test")

        count_before = PostIndex.count()
        post.delete()
        time.sleep(1)
        count_after = PostIndex.count()

        self.assertEqual(count_after, count_before - 1)

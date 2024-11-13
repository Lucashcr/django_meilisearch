"""
Test cases for the Meilisearch signals.
"""

import time
from django.test import TestCase

from api.models import Post
from api.indexes import PostIndex
from django_meilisearch.indexes import BaseIndex


class TestMeilisearchSignals(TestCase):
    """
    Test cases for the Meilisearch signals.
    It's responsible for testing the signals
    that are triggered when a model is created,
    updated or deleted.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test data.
        """
        PostIndex.create()
    
    def setUp(self):
        """
        Set up the test cases.
        """
        PostIndex.clean()

    def test_add_single_document_signal(self):
        """
        Test the addition of a single document.
        """
        count_before = PostIndex.count()
        Post.objects.create(title="Testing post", content="It's a testing post.")
        time.sleep(1)
        count_after = PostIndex.count()

        self.assertEqual(count_after, count_before + 1)

    def test_remove_single_document_signal(self):
        """
        Test the removal of a single document.
        """
        post = Post.objects.create(title="Testing post", content="It's a testing post.")

        count_before = PostIndex.count()
        post.delete()
        time.sleep(1)
        count_after = PostIndex.count()

        self.assertEqual(count_after, count_before - 1)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the test data.
        """
        PostIndex.destroy()

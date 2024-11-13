"""
Test cases for the CLI actions.
"""

import time

from django.test import TestCase
from meilisearch.errors import MeilisearchApiError

from example.indexes import PostIndex
from example.models import Post
from django_meilisearch import client


# Create your tests here.
class TestInitialize(TestCase):
    """
    Test cases for the CLI actions.
    """

    fixtures = ["posts.json"]

    def test_success_config(self):
        """
        Test the success of the configuration.
        """
        health = client.is_healthy()
        self.assertTrue(health)

    def test_create_index(self):
        """
        Test the creation of the index.
        """
        PostIndex.create()

        index = client.get_index(PostIndex.name)
        self.assertEqual(index.get_primary_key(), "id")
        self.assertEqual(index.uid, PostIndex.name)

        PostIndex.destroy()

    def test_populate_index(self):
        """
        Test the population of the index.
        """
        PostIndex.create()
        PostIndex.populate()
        count = PostIndex.count()

        index = client.get_index(PostIndex.name)
        self.assertEqual(index.get_primary_key(), "id")
        self.assertEqual(index.uid, PostIndex.name)
        self.assertEqual(count, Post.objects.count())

        PostIndex.destroy()

    def test_apopulate_index(self):
        """
        Test the population of the index.
        """
        PostIndex.create()
        tasks = PostIndex.apopulate()
        self.assertEqual(len(tasks), 1)
        self.assertTrue(all(task.status == "enqueued" for task in tasks))

        time.sleep(1)

        index = client.get_index(PostIndex.name)
        self.assertEqual(index.get_primary_key(), "id")
        self.assertEqual(index.uid, PostIndex.name)
        self.assertEqual(PostIndex.count(), Post.objects.count())

        PostIndex.destroy()

    def test_clean_index(self):
        """
        Test the cleaning of the index.
        """
        PostIndex.create()
        PostIndex.populate()
        pre_count = PostIndex.count()

        PostIndex.clean()
        post_count = PostIndex.count()

        self.assertEqual(pre_count, Post.objects.count())
        self.assertEqual(post_count, 0)

        PostIndex.destroy()

    def test_destroy_index(self):
        """
        Test the destruction of the index.
        """
        PostIndex.create()

        index = client.get_index(PostIndex.name)
        self.assertIsNotNone(index)

        PostIndex.destroy()

        with self.assertRaises(MeilisearchApiError):
            client.get_index(PostIndex.name)

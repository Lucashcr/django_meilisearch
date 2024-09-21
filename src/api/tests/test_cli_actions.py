"""
Test cases for the CLI actions.
"""

import json

from django.test import TestCase
from meilisearch.errors import MeilisearchApiError

from api.index import PostIndex
from api.models import Post
from django_meilisearch import client


# Create your tests here.
class TestInitialize(TestCase):
    """
    Test cases for the CLI actions.
    """

    def setUp(self):
        """
        Setup the test environment for the CLI action test cases.
        """
        with open("src/api/tests/data/posts.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            Post.objects.bulk_create([Post(**post) for post in data])

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

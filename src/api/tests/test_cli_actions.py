import json

from django.test import TestCase

from django_meilisearch import client

from meilisearch.errors import MeilisearchApiError

from api.documents import PostIndex
from api.models import Post


# Create your tests here.
class TestInitialize(TestCase):
    def setUp(self) -> None:
        data = json.load(open("src/api/tests/data/posts.json"))
        Post.objects.bulk_create([Post(**post) for post in data])
    
    def test_success_config(self):
        health = client.is_healthy()
        self.assertTrue(health)
    
    def test_create_index(self):
        PostIndex.create()
        
        index = client.get_index(PostIndex.name)
        self.assertEqual(index.get_primary_key(), "id")
        self.assertEqual(index.uid, PostIndex.name)
    
    def test_populate_index(self):
        PostIndex.create()
        PostIndex.populate()
        count = PostIndex.count()
        
        index = client.get_index(PostIndex.name)
        self.assertEqual(index.get_primary_key(), "id")
        self.assertEqual(index.uid, PostIndex.name)
        self.assertEqual(count, Post.objects.count())
    
    def test_clean_index(self):
        PostIndex.create()
        PostIndex.populate()
        pre_count = PostIndex.count()
        
        PostIndex.clean()
        post_count = PostIndex.count()
        
        self.assertEqual(pre_count, Post.objects.count())
        self.assertEqual(post_count, 0)
    
    def test_destroy_index(self):
        PostIndex.create()
        
        index = client.get_index(PostIndex.name)
        self.assertIsNotNone(index)
        
        PostIndex.destroy()
        
        with self.assertRaises(MeilisearchApiError):
            client.get_index(PostIndex.name)

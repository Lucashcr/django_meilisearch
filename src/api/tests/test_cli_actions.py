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
        task_info = PostIndex.create()
        
        task = client.get_task(task_info.task_uid)
        while task.status in ["enqueued", "processing"]:
            task = client.get_task(task_info.task_uid)
        
        index = client.get_index(PostIndex.name)
        self.assertEqual(index.get_primary_key(), "id")
        self.assertEqual(index.uid, PostIndex.name)
    
    def test_populate_index(self):
        task_info = PostIndex.create()
        task = client.get_task(task_info.task_uid)
        while task.status in ["enqueued", "processing"]:
            task = client.get_task(task_info.task_uid)
        
        count = PostIndex.populate()
        
        index = client.get_index(PostIndex.name)
        self.assertEqual(index.get_primary_key(), "id")
        self.assertEqual(index.uid, PostIndex.name)
        self.assertEqual(count, Post.objects.count())
    
    def test_clean_index(self):
        task_info = PostIndex.create()
        task = client.get_task(task_info.task_uid)
        while task.status in ["enqueued", "processing"]:
            task = client.get_task(task_info.task_uid)
        
        PostIndex.populate()
        
        index = client.get_index(PostIndex.name)
        count = index.get_stats().number_of_documents
        
        clean_count = PostIndex.clean()
        
        self.assertEqual(clean_count, count)
        self.assertEqual(index.get_stats().number_of_documents, 0)
    
    def test_destroy_index(self):
        task_info = PostIndex.create()
        task = client.get_task(task_info.task_uid)
        while task.status in ["enqueued", "processing"]:
            task = client.get_task(task_info.task_uid)
        
        index = client.get_index(PostIndex.name)
        self.assertIsNotNone(index)
        
        task_info = PostIndex.destroy()
        task = client.get_task(task_info.task_uid)
        while task.status in ["enqueued", "processing"]:
            task = client.get_task(task_info.task_uid)
        
        with self.assertRaises(MeilisearchApiError):
            client.get_index(PostIndex.name)

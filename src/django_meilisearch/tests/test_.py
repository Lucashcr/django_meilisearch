from django.test import TestCase


# Create your tests here.
class TestMeiliSearch(TestCase):
    def test_meilisearch(self):
        self.assertEqual(1+1, 2)

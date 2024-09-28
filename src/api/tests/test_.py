"""
Test cases for the MeiliSearch client
"""

from django.test import TransactionTestCase

from api.models import Post


# Create your tests here.
class TestMeiliSearch(TransactionTestCase):
    """
    Test cases for the MeiliSearch client
    """

    fixtures = ["posts.json"]

    def test_meilisearch(self):
        """
        Test the MeiliSearch client
        """
        count = Post.objects.count()
        self.assertEqual(count, 50)

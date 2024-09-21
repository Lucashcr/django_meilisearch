"""
Test cases for the MeiliSearch client
"""

from django.test import TestCase


# Create your tests here.
class TestMeiliSearch(TestCase):
    """
    Test cases for the MeiliSearch client
    """

    def test_meilisearch(self):
        """
        Test the MeiliSearch client
        """
        self.assertEqual(1 + 1, 2)

"""
Test cases for the instantiation of the index.
"""

from django.test import TestCase

from example.indexes import (
    PostIndex,
    PostIndexWithUseTimestamp,
    PostIndexWithoutUseTimestamp,
)


# Create your tests here.
class TestUseTimestampFlag(TestCase):
    """
    Test cases for the instantiation of the index.
    """

    fixtures = ["posts.json"]

    def test_default_use_timestamp_flag(self):
        """
        Test the success of the instance.
        """

        self.assertEqual(PostIndex.use_timestamp, False)

    def test_use_timestamp_flag_as_false(self):
        """
        Test the success of the instance.
        """

        PostIndexWithoutUseTimestamp.create()
        PostIndexWithoutUseTimestamp.populate()
        result = PostIndexWithoutUseTimestamp.search(
            "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            filter="id=1",
            limit=1,
        )
        print(result)
        PostIndexWithoutUseTimestamp.clean()
        PostIndexWithoutUseTimestamp.destroy()

        self.assertEqual(
            result["hits"][0]["created_at"], "2024-09-28T19:02:19.537000Z"
        )

    def test_use_timestamp_flag_as_true(self):
        """
        Test the success of the instance.
        """

        PostIndexWithUseTimestamp.create()
        PostIndexWithUseTimestamp.populate()
        result = PostIndexWithUseTimestamp.search(
            "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            filter="id=1",
            limit=1,
        )
        print(result)
        PostIndexWithUseTimestamp.clean()
        PostIndexWithUseTimestamp.destroy()

        self.assertEqual(result["hits"][0]["created_at"], 1727550139.537)

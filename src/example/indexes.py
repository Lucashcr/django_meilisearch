"""
This module contains the indexes definition for the api app.
"""

from django_meilisearch.indexes import BaseIndex

from example.models import Post
from example.serializers import PostSerializerWithTimestamp, PostSerializerWithoutTimestamp


class PostIndex(BaseIndex):
    """
    Index definition for the Post model.
    """

    name = "posts"
    model = Post
    # primary_key_field = "id"        # (default is models pk field)
    # searchable_fields = [...]       # (default is all fields in model)
    # filterable_fields = [...]       # (default is all fields in model)
    # sortable_fields = [...]         # (default is all fields in model)


class PostIndexWithUseTimestamp(BaseIndex):
    """
    Index definition for the Post model.
    """

    name = "posts_with_timestamp"
    model = Post
    serializer_class = PostSerializerWithTimestamp


class PostIndexWithoutUseTimestamp(BaseIndex):
    """
    Index definition for the Post model.
    """

    name = "posts_without_timestamp"
    model = Post
    serializer_class = PostSerializerWithoutTimestamp


class PostIndexWith10IndexingBatchSize(BaseIndex):
    """
    Index definition for the Post model.
    """

    name = "posts_without_timestamp"
    model = Post
    indexing_batch_size = 10

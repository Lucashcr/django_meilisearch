"""
This module contains the indexes definition for the api app.
"""

from django_meilisearch.indexes import BaseIndex

from example.models import Post


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
    use_timestamp = True


class PostIndexWithoutUseTimestamp(BaseIndex):
    """
    Index definition for the Post model.
    """

    name = "posts_without_timestamp"
    model = Post
    use_timestamp = False

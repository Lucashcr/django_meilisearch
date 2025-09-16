"""
Module for serializers used in the example application.
This module defines serializers for the Post model, including
serializers with and without timestamp fields.
"""

from rest_framework.serializers import ModelSerializer

from django_meilisearch.serializers.drf import TimestampField
from example.models import Post


class PostSerializerWithTimestamp(ModelSerializer):
    """
    Serializer for the Post model with a timestamp field.
    This serializer includes a custom TimestampField for the created_at field.
    """

    created_at = TimestampField()

    class Meta:
        model = Post
        fields = "__all__"


class PostSerializerWithoutTimestamp(ModelSerializer):
    """
    Serializer for the Post model without a timestamp field.
    This serializer does not include any custom fields.
    """

    class Meta:
        model = Post
        fields = "__all__"

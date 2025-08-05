from dataclasses import field
from rest_framework.serializers import ModelSerializer

from django_meilisearch.serializers.drf import TimestampField
from example.models import Post


class PostSerializerWithTimestamp(ModelSerializer):
    created_at = TimestampField()

    class Meta:
        model = Post
        fields = "__all__"


class PostSerializerWithoutTimestamp(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

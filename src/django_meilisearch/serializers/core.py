"""
Module for DjangoCoreSerializer, which serializes Django model instances
to a JSON format suitable for indexing.
"""

from datetime import datetime
import json

from django.core.serializers import serialize


# pylint: disable=too-few-public-methods
class DjangoCoreSerializer:
    """
    Base serializer for Django models to handle serialization to JSON.
    This serializer is used to convert Django model instances
    into a format suitable for indexing.
    It serializes the queryset and ensures that the primary key field
    is included in the serialized data.
    """

    def __init__(self, primary_key_field, use_timestamp, datetime_fields):
        self.primary_key_field = primary_key_field
        self.use_timestamp = use_timestamp
        self.datetime_fields = datetime_fields

    def serialize(self, queryset):
        """
        Serialize the queryset to JSON format.
        :param queryset: The queryset to serialize.
        """
        result = json.loads(serialize("json", queryset))

        serialized_data = []
        for obj in result:
            if not self.primary_key_field in obj["fields"]:
                obj["fields"][self.primary_key_field] = obj["pk"]

            if self.use_timestamp:
                for field, value in filter(
                    lambda item: item[0] in self.datetime_fields,
                    obj["fields"].items(),
                ):
                    parsed_datetime = datetime.fromisoformat(value)
                    obj["fields"][field] = parsed_datetime.timestamp()

            serialized_data.append(obj["fields"])

        return serialized_data

import json
from typing import Any

from django.core.serializers import serialize


class DjangoCoreSerializer:
    """
    Base serializer for Django models to handle serialization to JSON.
    This serializer is used to convert Django model instances into a format suitable for indexing.
    It serializes the queryset and ensures that the primary key field is included in the serialized data.
    """

    def __init__(self, primary_key_field):
        self.primary_key_field = primary_key_field
    
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
            serialized_data.append(obj["fields"])

        return serialized_data

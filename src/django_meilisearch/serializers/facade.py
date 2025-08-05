"""
Module for SerializerFacade, which provides a unified interface
for different serializer implementations.
"""

from typing import Iterable

from django.db.models import Model
from django_meilisearch.serializers.core import DjangoCoreSerializer


# pylint: disable=too-few-public-methods
class SerializerFacade:
    """
    Facade for serializers to provide a unified interface.
    This class abstracts the underlying serializer implementation
    and provides a consistent method to serialize data.
    """

    def __init__(
        self,
        serializer_class=None,
        primary_key_field=None,
        use_timestamp=False,
        datetime_fields=None,
    ):
        if serializer_class is not None:
            self.serializer_class = serializer_class
            self.type = "drf"
            return

        if primary_key_field is not None:
            self.serializer = DjangoCoreSerializer(
                primary_key_field, use_timestamp, datetime_fields
            )
            self.type = "core"
            return

        raise ValueError(
            "Either serializer_class or primary_key_field must be provided."
        )

    def serialize(self, queryset: Iterable[Model]):
        """
        Serialize the queryset using the underlying serializer.

        Args:
            :queryset: The queryset to serialize.

        Returns:
            :list[dict[str, Any]]: Serialized data as a list of dictionaries.

        Raises:
            :ValueError: If the serializer type is invalid.
        """
        if self.type == "drf":
            return self.serializer_class(queryset, many=True).data

        if self.type == "core":
            return self.serializer.serialize(queryset)

        raise ValueError("Invalid serializer type.")

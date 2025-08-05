"""
This module defines the Document metaclass that is used to create the Document class.

The Document class is used to define the structure of the index that will be created in MeiliSearch.
"""

from typing import Type
from weakref import WeakValueDictionary

from django.db.models import Model, signals

from django_meilisearch.exceptions import (
    InvalidDjangoModelError,
    InvalidIndexNameError,
    MissingRequiredFieldError,
)
from django_meilisearch.serializers.facade import SerializerFacade
from django_meilisearch.utils import (
    exists_field_in_namespace,
    get_datetime_fields,
)
from django_meilisearch.validators import (
    validate_drf_serializer,
    validate_filterable_fields,
    validate_primary_key_field,
    validate_searchable_fields,
    validate_sortable_fields,
)


class BaseIndexMetaclass(type):
    """
    The metaclass for the BaseIndex class.
    """

    __REQUIRED_FIELDS__ = [
        "name",
        "model",
    ]

    REGISTERED_INDEXES: dict[str, Type] = WeakValueDictionary()
    INDEX_NAMES: dict[str, str] = {}

    # pylint: disable=unused-argument
    @staticmethod
    def post_save_handler(sender, instance, **kwargs):
        """
        The post_save signal handler that adds the document to the index.
        """
        for index in BaseIndexMetaclass.REGISTERED_INDEXES.values():
            if isinstance(instance, index.model):
                index.aadd_single_document(instance)

    # pylint: disable=unused-argument
    @staticmethod
    def post_delete_handler(sender, instance, **kwargs):
        """
        The post_delete signal handler that removes the document from the index.
        """
        for index in BaseIndexMetaclass.REGISTERED_INDEXES.values():
            if isinstance(instance, index.model):
                index.aremove_single_document(instance)

    # pylint: disable=too-many-locals
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        """
        The new method of the metaclass that validates the fields of the class.
        """
        if name != "BaseIndex":
            if any(
                not exists_field_in_namespace(field, namespace)
                for field in BaseIndexMetaclass.__REQUIRED_FIELDS__
            ):
                raise MissingRequiredFieldError(
                    f"{name} must have at least {BaseIndexMetaclass.__REQUIRED_FIELDS__} fields"
                )

            model = namespace["model"]

            if not isinstance(namespace["name"], str):
                raise InvalidIndexNameError(f"{name}.name must be a string")

            if not issubclass(model, Model):
                raise InvalidDjangoModelError(
                    f"{name}.model must be a Django Model"
                )

            model_field_names = [field.name for field in model._meta.fields]

            searchable_fields = namespace.get("searchable_fields")
            if not searchable_fields or searchable_fields == "__all__":
                searchable_fields = model_field_names

            filterable_fields = namespace.get("filterable_fields")
            if not filterable_fields or filterable_fields == "__all__":
                filterable_fields = model_field_names

            sortable_fields = namespace.get("sortable_fields")
            if not sortable_fields or sortable_fields == "__all__":
                sortable_fields = model_field_names

            primary_key_field = namespace.get(
                "primary_key_field", model._meta.pk.name
            )

            validate_primary_key_field(model, primary_key_field)
            validate_searchable_fields(model, searchable_fields)
            validate_filterable_fields(model, filterable_fields)
            validate_sortable_fields(model, sortable_fields)

            signals.post_save.connect(mcs.post_save_handler, sender=model)
            signals.post_delete.connect(mcs.post_delete_handler, sender=model)

            cls = super().__new__(mcs, name, bases, namespace)

            cls.primary_key_field = primary_key_field
            cls.searchable_fields = searchable_fields
            cls.filterable_fields = filterable_fields
            cls.sortable_fields = sortable_fields

            serializer_class = namespace.get("serializer_class")
            if serializer_class is not None:
                validate_drf_serializer(name, serializer_class)
                cls.serializer = SerializerFacade(
                    serializer_class=serializer_class,
                )
            else:
                datetime_fields = (
                    get_datetime_fields(model)
                    if namespace.get("use_timestamp", False)
                    else []
                )
                cls.serializer = SerializerFacade(
                    primary_key_field=primary_key_field,
                    use_timestamp=namespace.get("use_timestamp", False),
                    datetime_fields=datetime_fields,
                )

            index_label = f"{namespace['model']._meta.app_label}.{namespace['__qualname__']}"
            mcs.REGISTERED_INDEXES[index_label] = cls
            mcs.INDEX_NAMES[namespace["name"]] = index_label
            return cls

        return super().__new__(mcs, name, bases, namespace)

    def __del__(cls):
        """
        The delete method of the metaclass that removes the signal handlers.
        """

        signals.post_save.disconnect(
            BaseIndexMetaclass.post_save_handler, sender=cls.model
        )
        signals.post_delete.disconnect(
            BaseIndexMetaclass.post_delete_handler, sender=cls.model
        )

        if cls.name in BaseIndexMetaclass.INDEX_NAMES:
            del BaseIndexMetaclass.INDEX_NAMES[cls.name]

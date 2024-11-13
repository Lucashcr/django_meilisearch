"""
This module defines the Document metaclass that is used to create the Document class.

The Document class is used to define the structure of the index that will be created in MeiliSearch.
"""

from typing import Type
from weakref import WeakValueDictionary

from django.db.models import Model, signals, DateTimeField
from rest_framework.serializers import ModelSerializer

from django_meilisearch.exceptions import (
    InvalidDjangoModelError,
    InvalidIndexNameError,
    InvalidPrimaryKeyError,
    MissingRequiredFieldError,
)
from django_meilisearch.utils import exists_field_in_namespace
from django_meilisearch.validators import (
    validate_filterable_fields,
    validate_searchable_fields,
    validate_sortable_fields,
)
from django_meilisearch.serializers import TimestampField


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
            searchable_fields = namespace.get(
                "searchable_fields", model_field_names
            )
            filterable_fields = namespace.get(
                "filterable_fields", model_field_names
            )
            sortable_fields = namespace.get(
                "sortable_fields", model_field_names
            )

            primary_key_field = namespace.get(
                "primary_key_field", model._meta.pk.name
            )

            if not isinstance(primary_key_field, str):
                raise InvalidPrimaryKeyError(
                    f"{name}.Django.primary_key_field must be a string"
                )

            if not hasattr(model, primary_key_field):
                raise InvalidPrimaryKeyError(
                    f"{model.__name__} does not have a"
                    f"primary_key_field named {primary_key_field}"
                )

            validate_searchable_fields(
                name, searchable_fields, model_field_names, model
            )
            validate_filterable_fields(
                name, filterable_fields, model_field_names, model
            )
            validate_sortable_fields(
                name, sortable_fields, model_field_names, model
            )

            signals.post_save.connect(mcs.post_save_handler, sender=model)
            signals.post_delete.connect(mcs.post_delete_handler, sender=model)

            cls = super().__new__(mcs, name, bases, namespace)

            cls.primary_key_field = primary_key_field
            cls.searchable_fields = searchable_fields
            cls.filterable_fields = filterable_fields
            cls.sortable_fields = sortable_fields

            Meta = type(
                "Meta",
                (),
                {"model": model, "fields": model_field_names},
            )

            datetime_fields = {}
            for field_name in model_field_names:
                field_class = getattr(model, field_name)
                if isinstance(field_class.field, DateTimeField):
                    datetime_fields[field_name] = TimestampField()

            cls.serializer = type(
                f"{name}Serializer",
                (ModelSerializer,),
                {"Meta": Meta, **datetime_fields},
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

"""
This module defines the Document metaclass that is used to create the Document class.

The Document class is used to define the structure of the index that will be created in MeiliSearch.
"""

from typing import Type

from django.db.models import Model, signals
from djantic import ModelSchema
from pydantic import ConfigDict

from django_meilisearch.exceptions import (
    InvalidDjangoModelError,
    InvalidFilterableFieldError,
    InvalidIndexNameError,
    InvalidPrimaryKeyError,
    InvalidSearchableFieldError,
    InvalidSortableFieldError,
    MissingRequiredFieldError,
)
from django_meilisearch.utils import exists_field_in_namespace
from django_meilisearch.validators import (
    validate_filterable_fields,
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

    REGISTERED_INDEXES: dict[str, Type] = {}
    INDEX_NAMES: dict[str, str] = {}

    @staticmethod
    def post_save_handler(_, instance, **kwargs):
        """
        The post_save signal handler that adds the document to the index.
        """
        for _, index in BaseIndexMetaclass.REGISTERED_INDEXES.items():
            if isinstance(instance, index.model):
                index.add_single_document(instance)

    @staticmethod
    def post_delete_handler(_, instance, **kwargs):
        """
        The post_delete signal handler that removes the document from the index.
        """
        for _, index in BaseIndexMetaclass.REGISTERED_INDEXES.items():
            if isinstance(instance, index.model):
                index.remove_single_document(instance)

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

            model_field_names = [field.name for field in model._meta.fields]
            searchable_fields = namespace.get("searchable_fields", model_field_names)
            filterable_fields = namespace.get("filterable_fields", model_field_names)
            sortable_fields = namespace.get("sortable_fields", model_field_names)

            if not isinstance(namespace["name"], str):
                raise InvalidIndexNameError(f"{name}.name must be a string")

            if not issubclass(model, Model):
                raise InvalidDjangoModelError(f"{name}.model must be a Django Model")

            mcs.primary_key_field = getattr(
                namespace, "primary_key_field", model._meta.pk.name
            )

            if not isinstance(mcs.primary_key_field, str):
                raise InvalidPrimaryKeyError(
                    f"{name}.Django.primary_key_field must be a string"
                )
            if not hasattr(model, mcs.primary_key_field):
                raise InvalidPrimaryKeyError(
                    f"{model.__name__} does not have a"
                    f"primary_key_field named {mcs.primary_key_field}"
                )

            validate_searchable_fields(name, searchable_fields, model_field_names)
            validate_filterable_fields(name, filterable_fields, model_field_names)
            validate_sortable_fields(name, sortable_fields, model_field_names)

            for field in searchable_fields:
                if not hasattr(model, field):
                    raise InvalidSearchableFieldError(
                        f"{model.__name__} does not have a searchable_field named {field}"
                    )

            for field in filterable_fields:
                if not hasattr(model, field):
                    raise InvalidFilterableFieldError(
                        f"{model.__name__} does not have a filterable_field named {field}"
                    )

            for field in sortable_fields:
                if not hasattr(model, field):
                    raise InvalidSortableFieldError(
                        f"{model.__name__} does not have a filterable_field named {field}"
                    )

            signals.post_save.connect(mcs.post_save_handler, sender=model)
            signals.post_delete.connect(mcs.post_delete_handler, sender=model)

            mcs.searchable_fields = searchable_fields
            mcs.filterable_fields = filterable_fields
            mcs.sortable_fields = sortable_fields

            mcs.schema: ModelSchema = type(
                f"{name}Schema",
                (ModelSchema,),
                {
                    "model_config": ConfigDict(
                        model=model,  # type: ignore
                    )
                },
            )

            index_label = (
                f"{namespace['model']._meta.app_label}.{namespace['__qualname__']}"
            )
            mcs.REGISTERED_INDEXES[index_label] = super().__new__(
                mcs, name, bases, namespace
            )
            mcs.INDEX_NAMES[namespace["name"]] = index_label
            return mcs.REGISTERED_INDEXES[index_label]

        return super().__new__(mcs, name, bases, namespace)

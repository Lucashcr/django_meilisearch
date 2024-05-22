from django.db.models import Model

from meilisearchdsl import Q

from django_meilisearch import client
from django_meilisearch.exceptions import *
from django_meilisearch.serializers import serialize_queryset
from django_meilisearch.utils import convert_to_camel_case, exists_field_in_namespace


class DocType(type):
    __REQUIRED_FIELDS__ = [
        "name",
        "Django__model",
    ]

    REGISTERED_INDEXES = {}

    def __new__(cls, name: str, bases: tuple, namespace: dict):
        result = super().__new__(cls, name, bases, namespace)

        if name != "Document":
            if any(
                not exists_field_in_namespace(field, namespace)
                for field in DocType.__REQUIRED_FIELDS__
            ):
                raise MissingRequiredFieldError(f"{name} must have at least {DocType.__REQUIRED_FIELDS__} fields")

            model = namespace["Django"].model
            
            model_field_names = [field.name for field in model._meta.fields]
            searchable_fields = getattr(
                namespace["Django"], "searchable_fields", model_field_names
            )
            
            filterable_fields = getattr(
                namespace["Django"], "filterable_fields", model_field_names
            )
            
            if not isinstance(namespace["name"], str):
                raise InvalidIndexNameError(f"{name}.name must be a string")

            if not issubclass(model, Model):
                raise InvalidDjangoModelError(f"{name}.Django.model must be a Django Model")
            
            if not hasattr(namespace["Django"], "primary_key_field"):
                namespace["Django"].primary_key_field = model._meta.pk.name
            
            if not isinstance(namespace["Django"].primary_key_field, str):
                raise InvalidPrimaryKeyError(f"{name}.Django.primary_key_field must be a string")

            if not isinstance(searchable_fields, list):
                if (
                    isinstance(searchable_fields, str)
                    and searchable_fields == "__all__"
                ):
                    searchable_fields = model_field_names
                else:
                    raise InvalidSearchableFieldError(
                        f"{name}.Django.searchable_fields must be a list or '__all__'"
                    )

                raise InvalidSearchableFieldError(f"{name}.Django.searchable_fields must be a list ")

            if not isinstance(filterable_fields, list):
                if (
                    isinstance(filterable_fields, str)
                    and filterable_fields == "__all__"
                ):
                    filterable_fields = model_field_names
                else:
                    raise InvalidFilterableFieldError(
                        f"{name}.Django.filterable_fields must be a list or '__all__'"
                    )
                
                raise InvalidFilterableFieldError(f"{name}.Django.filterable_fields must be a list ")

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

            namespace["Django"].searchable_fields = searchable_fields
            namespace["Django"].filterable_fields = filterable_fields
            
            index_label = f"{model._meta.app_label}.{namespace['__qualname__']}"
            cls.REGISTERED_INDEXES[index_label] = result

        return result

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

    def create(cls):
        client.get_index(
            cls.name,
            {
                "primaryKey": cls.Django.primary_key_field,
            },
        )

    def populate(cls):
        index = client.get_index(cls.name, cls.Django.primary_key_field)

        model_field_names = [field.name for field in cls.Django.model._meta.fields]
        index.aupdate_filterable_attributes(model_field_names)
        index.aupdate_searchable_attributes(model_field_names)

        db_count = cls.Django.model.objects.count()

        for i in range(0, db_count, 1000):
            batch = cls.Django.model.objects.all()[i : i + 1000]
            index.aadd_documents(
                serialize_queryset(batch, cls.Django.model),
                cls.Django.primary_key_field,
            )

        return db_count

    def clean(cls):
        index = client.get_index(cls.name, cls.Django.primary_key_field)
        count = client.get_stats()["indexes"][cls.name]["numberOfDocuments"]
        index.adelete_all_documents()
        return count

    def search(cls, term: str, query: Q, **kwargs):
        index = client.get_index(cls.name, cls.Django.primary_key_field)
        for key in list(kwargs.keys()):
            camel_key = convert_to_camel_case(key)
            kwargs[camel_key] = kwargs[key]
            del kwargs[key]
        return index.search(term, q=query, opt_params=kwargs)


class Document(metaclass=DocType): ...

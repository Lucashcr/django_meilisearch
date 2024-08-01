from http import HTTPStatus
from typing_extensions import Unpack

from django.db.models import Model

from meilisearch.errors import MeilisearchApiError

from django_meilisearch import client
from django_meilisearch.exceptions import *
from django_meilisearch.serializers import serialize_queryset
from django_meilisearch.types import OptParams
from django_meilisearch.utils import convert_to_camel_case, exists_field_in_namespace


class DocType(type):
    __REQUIRED_FIELDS__ = [
        "name",
        "model",
    ]

    REGISTERED_INDEXES = {}

    def __new__(cls, name: str, bases: tuple, namespace: dict):
        if name != "Document":
            if any(
                not exists_field_in_namespace(field, namespace)
                for field in DocType.__REQUIRED_FIELDS__
            ):
                raise MissingRequiredFieldError(f"{name} must have at least {DocType.__REQUIRED_FIELDS__} fields")

            model = namespace["model"]
            
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
            
            if not isinstance(namespace["name"], str):
                raise InvalidIndexNameError(f"{name}.name must be a string")

            if not issubclass(model, Model):
                raise InvalidDjangoModelError(f"{name}.model must be a Django Model")
            
            cls.primary_key_field = getattr(namespace, "primary_key_field", model._meta.pk.name)
            
            if not isinstance(cls.primary_key_field, str):
                raise InvalidPrimaryKeyError(f"{name}.Django.primary_key_field must be a string")
            if not hasattr(model, cls.primary_key_field):
                raise InvalidPrimaryKeyError(f"{model.__name__} does not have a primary_key_field named {cls.primary_key_field}")

            if not isinstance(searchable_fields, list):
                if (
                    isinstance(searchable_fields, str)
                    and searchable_fields == "__all__"
                ):
                    searchable_fields = model_field_names
                else:
                    raise InvalidSearchableFieldError(
                        f"{name}.searchable_fields must be a list or '__all__'"
                    )

                raise InvalidSearchableFieldError(f"{name}.searchable_fields must be a list or '__all__'")

            if not isinstance(filterable_fields, list):
                if (
                    isinstance(filterable_fields, str)
                    and filterable_fields == "__all__"
                ):
                    filterable_fields = model_field_names
                else:
                    raise InvalidFilterableFieldError(
                        f"{name}.filterable_fields must be a list or '__all__'"
                    )
                
                raise InvalidFilterableFieldError(f"{name}.filterable_fields must be a list or '__all__'")

            if not isinstance(sortable_fields, list):
                if (
                    isinstance(sortable_fields, str)
                    and sortable_fields == "__all__"
                ):
                    sortable_fields = model_field_names
                else:
                    raise InvalidSortableFieldError(
                        f"{name}.sortable_fields must be a list or '__all__'"
                    )
                
                raise InvalidSortableFieldError(f"{name}.sortable_fields must be a list or '__all__'")

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

            cls.searchable_fields = searchable_fields
            cls.filterable_fields = filterable_fields
            cls.sortable_fields = sortable_fields
            
            index_label = f"{namespace['model']._meta.app_label}.{namespace['__qualname__']}"
            cls.REGISTERED_INDEXES[index_label] = super().__new__(cls, name, bases, namespace)
            return cls.REGISTERED_INDEXES[index_label]

        return super().__new__(cls, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

    def create(cls):
        client.create_index(
            cls.name,
            {"primaryKey": cls.primary_key_field}
        )

    def populate(cls) -> int:
        index = client.get_index(cls.name)

        index.update_filterable_attributes(cls.filterable_fields)
        index.update_searchable_attributes(cls.searchable_fields)
        index.update_sortable_attributes(cls.sortable_fields)

        db_count = cls.model.objects.count()

        for i in range(0, db_count, 1000):
            batch = cls.model.objects.all()[i : i + 1000]
            index.add_documents(
                serialize_queryset(batch, cls.model),
                cls.primary_key_field,
            )

        return db_count

    def clean(cls) -> int:
        index = client.get_index(cls.name)
        count = client.get_all_stats()["indexes"][cls.name]["numberOfDocuments"]
        index.delete_all_documents()
        return count

    def search(cls, term: str, **opt_params: Unpack[OptParams]):
        if not "attributes_to_search_on" in opt_params:
            opt_params["attributes_to_search_on"] = cls.searchable_fields
        
        for key in list(opt_params.keys()):
            camel_key = convert_to_camel_case(key)
            if camel_key != key:
                opt_params[camel_key] = opt_params[key]
                del opt_params[key]
        try:
            index = client.get_index(cls.name)
            results = index.search(term, opt_params=opt_params)
        
        except MeilisearchApiError as e:
            results = {**e.__dict__}
            status_code = e.status_code if e.status_code else HTTPStatus.INTERNAL_SERVER_ERROR
        
        else:
            status_code = HTTPStatus.OK if results.get("hits") else HTTPStatus.NOT_FOUND
        
        finally:
            return results, status_code


class Document(metaclass=DocType): ...

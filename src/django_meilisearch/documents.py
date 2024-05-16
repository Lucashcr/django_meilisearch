from django.db.models import Model

from meilisearchdsl import Q

from django_meilisearch import client
from django_meilisearch.serializers import serialize_queryset
from django_meilisearch.utils import convert_to_camel_case, exists_field_in_namespace


class DocType(type):
    __REQUIRED_FIELDS__ = [
        "name",
        "Django__model",
        "Django__primary_key_field",
    ]

    REGISTERED_INDEXES = {}

    def __new__(cls, name: str, bases: tuple, namespace: dict):
        result = super().__new__(cls, name, bases, namespace)

        if name != "Document":
            if any(
                not exists_field_in_namespace(field, namespace)
                for field in DocType.__REQUIRED_FIELDS__
            ):
                raise ValueError(f"{name} must have {DocType.__REQUIRED_FIELDS__}")

            model = namespace["Django"].model
            search_fields = namespace["Django"].search_fields

            if not model:
                raise ValueError(f"{name}.Django.model must be defined")

            if search_fields is not None:
                search_fields = []

            if not isinstance(search_fields, list):
                if isinstance(search_fields, str):
                    if search_fields == "__all__":
                        search_fields = [model._meta.fields]
                    else:
                        raise ValueError(
                            f"{name}.Django.search_fields must be a list or '__all__'"
                        )

                raise ValueError(f"{name}.Django.search_fields must be a list ")

            if not issubclass(model, Model):
                raise ValueError(f"{name}.Django.model must be a Django Model")

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

        model_fields = [field.name for field in cls.Django.model._meta.fields]
        index.aupdate_filterable_attributes(model_fields)
        index.aupdate_searchable_attributes(model_fields)

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

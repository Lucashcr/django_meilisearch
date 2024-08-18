from http import HTTPStatus
from typing_extensions import Unpack

from meilisearch.errors import MeilisearchApiError

from django_meilisearch import client
from django_meilisearch.exceptions import *
from django_meilisearch.types import OptParams
from django_meilisearch.utils import convert_to_camel_case
from django_meilisearch.doctype import DocType


class Document(metaclass=DocType):
    @classmethod
    def create(cls):
        client.create_index(
            cls.name,
            {"primaryKey": cls.primary_key_field}
        )

    @classmethod
    def populate(cls) -> int:
        index = client.get_index(cls.name)

        index.update_filterable_attributes(cls.filterable_fields)
        index.update_searchable_attributes(cls.searchable_fields)
        index.update_sortable_attributes(cls.sortable_fields)

        db_count = cls.model.objects.count()

        for i in range(0, db_count, 1000):
            batch = cls.model.objects.all()[i : i + 1000]
            index.add_documents(
                [s.model_dump(mode='json') for s in cls.schema.from_django(batch, many=True)],
                cls.primary_key_field,
            )

        return db_count

    @classmethod
    def clean(cls) -> int:
        index = client.get_index(cls.name)
        count = client.get_all_stats()["indexes"][cls.name]["numberOfDocuments"]
        index.delete_all_documents()
        return count

    @classmethod
    def search(cls, term: str, **opt_params: Unpack[OptParams]):
        if not opt_params.get("attributes_to_search_on"):
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

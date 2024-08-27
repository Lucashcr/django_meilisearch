from http import HTTPStatus
from typing_extensions import Unpack

from alive_progress import alive_bar

from django_meilisearch import client
from django_meilisearch.exceptions import *
from django_meilisearch.types import OptParams
from django_meilisearch.utils import convert_to_camel_case
from django_meilisearch.doctype import DocType

from meilisearch.errors import MeilisearchApiError


class Document(metaclass=DocType):
    @classmethod
    def __await_task_completion(cls, task_uid):
        task = client.get_task(task_uid)
        while task.status in ["enqueued", "processing"]:
            task = client.get_task(task_uid)
        return task
    
    @classmethod
    def acreate(cls):
        task_info = client.create_index(
            cls.name,
            {"primaryKey": cls.primary_key_field}
        )
        return client.get_task(task_info.task_uid)
    
    @classmethod
    def create(cls):
        task = cls.acreate()
        return cls.__await_task_completion(task.uid)
    
    @classmethod
    def apopulate(cls) -> int:
        index = client.get_index(cls.name)

        index.update_filterable_attributes(cls.filterable_fields)
        index.update_searchable_attributes(cls.searchable_fields)
        index.update_sortable_attributes(cls.sortable_fields)

        db_count = cls.model.objects.count()

        tasks = []
        with alive_bar(db_count, title=f"Indexing {cls.name}") as progress:
            for i in range(0, db_count, 1000):
                batch = cls.model.objects.all()[i : i + 1000]
                task_info = index.add_documents(
                    [s.model_dump(mode='json') for s in cls.schema.from_django(batch, many=True)],
                    cls.primary_key_field,
                )
                task = client.get_task(task_info.task_uid)
                tasks.append(task)
                progress(batch.count())
        
        return tasks
    
    @classmethod
    def populate(cls) -> int:
        index = client.get_index(cls.name)

        index.update_filterable_attributes(cls.filterable_fields)
        index.update_searchable_attributes(cls.searchable_fields)
        index.update_sortable_attributes(cls.sortable_fields)

        db_count = cls.model.objects.count()

        tasks = []
        with alive_bar(db_count, title=f"Indexing {cls.name}") as progress:
            for i in range(0, db_count, 1000):
                batch = cls.model.objects.all()[i : i + 1000]
                task_info = index.add_documents(
                    [s.model_dump(mode='json') for s in cls.schema.from_django(batch, many=True)],
                    cls.primary_key_field,
                )
                task = cls.__await_task_completion(task_info.task_uid)
                tasks.append(task)
                progress(batch.count())
        
        return tasks

    @classmethod
    def aclean(cls) -> int:
        index = client.get_index(cls.name)
        task_info = index.delete_all_documents()
        return client.get_task(task_info.task_uid)

    @classmethod
    def clean(cls) -> int:
        task = cls.aclean()
        return cls.__await_task_completion(task.uid)

    @classmethod
    def search(cls, term: str, to_queryset: bool = False, **opt_params: Unpack[OptParams]):
        if not opt_params.get("attributes_to_search_on"):
            opt_params["attributes_to_search_on"] = cls.searchable_fields
        
        for key in list(opt_params.keys()):
            camel_key = convert_to_camel_case(key)
            if camel_key != key:
                opt_params[camel_key] = opt_params[key]
                del opt_params[key]
        
        if 'attributesToRetrieve' in opt_params and cls.primary_key_field not in opt_params['attributesToRetrieve']:
            opt_params['attributesToRetrieve'] += [cls.primary_key_field]
        
        try:
            index = client.get_index(cls.name)
            results = index.search(term, opt_params=opt_params)
            
            if to_queryset:
                results['hits'] = cls.model.objects.filter(
                    pk__in=[hit[cls.primary_key_field] for hit in results['hits']]
                )
        
        except MeilisearchApiError as e:
            results = {**e.__dict__}
            status_code = e.status_code if e.status_code else HTTPStatus.INTERNAL_SERVER_ERROR
        
        else:
            status_code = HTTPStatus.OK if results.get("hits") else HTTPStatus.NOT_FOUND
        
        finally:
            return results, status_code
    
    @classmethod
    def adestroy(cls):
        task_info = client.delete_index(cls.name)
        return client.get_task(task_info.task_uid)

    @classmethod
    def destroy(cls):
        task = cls.adestroy()
        return cls.__await_task_completion(task.uid)
    
    @classmethod
    def aadd_single_document(cls, instance):
        index = client.index(cls.name)        
        task_info = index.add_documents(
            [cls.schema.from_django(instance).model_dump(mode='json')],
            cls.primary_key_field
        )
        return client.get_task(task_info.uid)

    @classmethod
    def add_single_document(cls, instance):
        task = cls.aadd_single_document(instance)
        return cls.__await_task_completion(task.uid)
    
    
    @classmethod
    def aremove_single_document(cls, instance):
        index = client.get_index(cls.name)
        task_info = index.delete_document(instance.pk)
        return client.get_task(task_info.task_uid)
    
    @classmethod
    def remove_single_document(cls, instance):
        task = cls.aremove_single_document(instance)
        return cls.__await_task_completion(task.uid)
    
    @classmethod
    def count(cls):
        index = client.get_index(cls.name)
        return index.get_stats().number_of_documents

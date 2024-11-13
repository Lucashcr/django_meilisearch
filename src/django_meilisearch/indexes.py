"""
This module contains the Document class, which provides methods for creating,
populating, rebuilding, deleting, cleaning and searching an index in MeiliSearch.
"""

from http import HTTPStatus
from typing import Iterable, Optional, Type
from typing_extensions import Unpack

from alive_progress import alive_bar
from camel_converter import dict_to_camel
from django.db.models import Model
from meilisearch.errors import MeilisearchApiError
from meilisearch.models.task import Task
from rest_framework.serializers import Serializer

from django_meilisearch import client
from django_meilisearch.types import OptParams
from django_meilisearch.metaclass import BaseIndexMetaclass


class BaseIndex(metaclass=BaseIndexMetaclass):
    """Index document for a Django model.

    Attributes:
        name (str): Index name.
        model (Type[Model]): Django model.
        primary_key_field (str): Primary key field of the model.
        Defaults to model's primary key field.
        searchable_fields (list[str]): Fields to search on.
        Defaults to all fields in the model.
        filterable_fields (list[str]): Fields to filter on.
        Defaults to all fields in the model.
        sortable_fields (list[str]): Fields to sort on.
        Defaults to all fields in the model.
    """

    name: str
    model: Type[Model]

    primary_key_field: Optional[str] = None
    searchable_fields: Optional[Iterable[str]] = None
    filterable_fields: Optional[Iterable[str]] = None
    sortable_fields: Optional[Iterable[str]] = None

    serializer: Type[Serializer]

    @classmethod
    def __await_task_completion(cls, task_uid: int) -> Task:
        """Wait for a task to complete.

        Args:
            task_uid (int): Task UID.

        Returns:
            Task: Meilisearch task object.
        """

        task = client.get_task(task_uid)
        while task.status in ["enqueued", "processing"]:
            task = client.get_task(task_uid)
        return task

    @classmethod
    def acreate(cls) -> Task:
        """Create the index asynchronously.

        Returns:
            Task: Meilisearch task object.
        """

        task_info = client.create_index(
            cls.name, {"primaryKey": cls.primary_key_field}
        )
        return client.get_task(task_info.task_uid)

    @classmethod
    def create(cls) -> Task:
        """Create the index.

        Returns:
            Task: Meiliseach task object.
        """

        task = cls.acreate()
        return cls.__await_task_completion(task.uid)

    @classmethod
    def apopulate(cls) -> list[Task]:
        """Populate the index asynchronously.
        The method will index the entire database in batches of 1000.

        Returns:
            list[Task]: List of Meilisearch task objects.
        """

        index = client.get_index(cls.name)

        index.update_filterable_attributes(cls.filterable_fields)
        index.update_searchable_attributes(cls.searchable_fields)
        index.update_sortable_attributes(cls.sortable_fields)

        db_count = cls.model.objects.count()

        tasks = []
        for i in range(0, db_count, 1000):
            batch = cls.model.objects.all()[i : i + 1000]
            task_info = index.add_documents(
                cls.serializer(batch, many=True).data,
                cls.primary_key_field,
            )
            task = client.get_task(task_info.task_uid)
            tasks.append(task)

        return tasks

    @classmethod
    def populate(cls) -> list[Task]:
        """Populate the index.
        The method will index the entire database in batches of 1000.

        Returns:
            list[Task]: List of Meilisearch task objects.
        """

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
                    cls.serializer(batch, many=True).data,
                    cls.primary_key_field,
                )
                task = cls.__await_task_completion(task_info.task_uid)
                tasks.append(task)
                progress(batch.count())  # pylint: disable=not-callable

        return tasks

    @classmethod
    def aclean(cls) -> Task:
        """Delete all documents from the index asynchronously.

        Returns:
            Task: Meilisearch task object.
        """

        index = client.get_index(cls.name)
        task_info = index.delete_all_documents()
        return client.get_task(task_info.task_uid)

    @classmethod
    def clean(cls) -> Task:
        """Delete all documents from the index.

        Returns:
            Task: Meilisearch task object.
        """

        task = cls.aclean()
        return cls.__await_task_completion(task.uid)

    @classmethod
    def search(
        cls, term: str, **opt_params: Unpack[OptParams]
    ) -> tuple[dict, HTTPStatus]:
        """Do a search on the index.

        Args:
            term (str): Search term.
            to_queryset (bool, optional): If True, the search results will be converted
            to Django model instances. Defaults to False.

        Returns:
            dict: Search results.
        """

        if not opt_params.get("attributes_to_search_on"):
            opt_params["attributes_to_search_on"] = cls.searchable_fields

        opt_params = dict_to_camel(opt_params)

        try:
            index = client.get_index(cls.name)
            results = index.search(term, opt_params=opt_params)

        except MeilisearchApiError as e:
            results = {"hits": [], **e.__dict__}

        return results

    @classmethod
    def adestroy(cls) -> Task:
        """Delete the index asynchronously.

        Returns:
            Task: Meilisearch task object.
        """

        task_info = client.delete_index(cls.name)
        return client.get_task(task_info.task_uid)

    @classmethod
    def destroy(cls) -> Task:
        """Delete the index.

        Returns:
            Task: Meilisearch task object.
        """

        task = cls.adestroy()
        return cls.__await_task_completion(task.uid)

    @classmethod
    def aadd_single_document(cls, instance: Model) -> Task:
        """Add a single document to the index asynchronously.

        Args:
            instance (django.db.models.Model): Django model instance.

        Returns:
            Task: Meilisearch task object.
        """

        index = client.index(cls.name)
        task_info = index.add_documents(
            [cls.serializer(instance).data],
            cls.primary_key_field,
        )
        return client.get_task(task_info.task_uid)

    @classmethod
    def add_single_document(cls, instance: Model) -> Task:
        """Add a single document to the index.

        Args:
            instance (django.db.models.Model): Django model instance.

        Returns:
            Task: Meilisearch task object.
        """

        task = cls.aadd_single_document(instance)
        return cls.__await_task_completion(task.uid)

    @classmethod
    def aremove_single_document(cls, instance: Model) -> Task:
        """Remove a single document from the index asynchronously.

        Args:
            instance (Model): Django model instance.

        Returns:
            Task: Meilisearch task object.
        """

        index = client.get_index(cls.name)
        task_info = index.delete_document(instance.pk)
        return client.get_task(task_info.task_uid)

    @classmethod
    def remove_single_document(cls, instance: Model) -> Task:
        """Remove a single document from the index.

        Args:
            instance (Model): Django model instance.

        Returns:
            Task: Meilisearch task object.
        """

        task = cls.aremove_single_document(instance)
        return cls.__await_task_completion(task.uid)

    @classmethod
    def count(cls) -> int:
        """Get the number of documents in the index.

        Returns:
            int: Number of documents in the index.
        """

        index = client.get_index(cls.name)
        return index.get_stats().number_of_documents

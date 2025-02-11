"""
This module contains the Document class, which provides methods for creating,
populating, rebuilding, deleting, cleaning and searching an index in MeiliSearch.
"""

from http import HTTPStatus
from typing import Any, Iterable, Optional, Type
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

    use_timestamp: bool = False
    indexing_batch_size: int = 100_000

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
        The method will index the entire database in batches of a number of documents
        specified by the `indexing_batch_size` attribute.

        Returns:
            list[Task]: List of Meilisearch task objects.
        """

        index = client.get_index(cls.name)

        index.update_filterable_attributes(cls.filterable_fields)
        index.update_searchable_attributes(cls.searchable_fields)
        index.update_sortable_attributes(cls.sortable_fields)

        db_count = cls.model.objects.count()

        tasks = []
        for i in range(0, db_count, cls.indexing_batch_size):
            batch = cls.model.objects.all()[i : i + cls.indexing_batch_size]
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
        The method will index the entire database in batches of a number of documents
        specified by the `indexing_batch_size` attribute.

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
            for i in range(0, db_count, cls.indexing_batch_size):
                batch = cls.model.objects.all()[
                    i : i + cls.indexing_batch_size
                ]
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
    ) -> dict[str, Any]:
        """Do a search on the index.

        Args:
            term (str): Define the search query term.
            limit (Optional[int]): Used with `offset` to paginate results, define the number of hits to return. (Default: 20)
            offset (Optional[int]): Used with `limit` to paginate results, define the offset of the first hit to return. (Default: 0)
            hits_per_page (Optional[int]): Used with `page` to paginate results, define the number of hits to return per page. (Default: 20)
            page (Optional[int]): Used with `hits_per_page` to paginate results, define the page to return. (Default: 1)
            filter (Optional[Union[str, list]]): Define the filter query for the search.
            facets (Optional[list[str]]): Define the list of attributes to retrieve facets.
            attributes_to_retrieve (Optional[list[str]]): Define the attributes to retrieve.
            attributes_to_crop (Optional[list[str]]): Define the attributes to crop and, if set, the length used to crop each attribute value.
            crop_length (Optional[int]): Define the length used to crop the attributes values. (Default: 10)
            crop_marker (Optional[str]): Define the characters used to crop the attributes values. (Default: "...")
            attributes_to_highlight (Optional[list[str]]): Define the attributes to highlight in the search results.
            highlight_pre_tag (Optional[str]): Define the string to insert before the highlighted parts in the attributes values. (Default: "<em>")
            highlight_post_tag (Optional[str]): Define the string to insert after the highlighted parts in the attributes values. (Default: "</em>")
            show_matches_position (Optional[bool]): Define whether to show the matches position in the attributes values. (Default: False)
            sort (Optional[list[str]]): Define the attributes to sort the search results.
            matching_strategy (Optional[str]): Defines the strategy used to match query terms in documents. (Default: "last")
            show_ranking_score (Optional[bool]): Define whether to show the ranking score in the search results. (Default: False)
            show_ranking_score_details (Optional[bool]): Define whether to show the ranking score details in the search results. (Default: False)
            ranking_score_threshold (Optional[float]): Define the threshold used to filter the search results.
            attributes_to_search_on (Optional[list[str]]): Define the attributes to search on. If not set, the default attributes to search on are used.

        Returns:
            dict: Search results.

        _(See the MeiliSearch documentation to learn more about the options available for the search method and their usage.)_

        https://www.meilisearch.com/docs/reference/api/search
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

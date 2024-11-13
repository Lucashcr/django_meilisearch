"""
Validators for the MeiliSearch index metaclass.
"""

from typing import Union

from django.db.models import Model

from django_meilisearch.exceptions import (
    InvalidFilterableFieldError,
    InvalidSearchableFieldError,
    InvalidSortableFieldError,
)


def validate_searchable_fields(
    name: str,
    searchable_fields: Union[str, list],
    model_field_names: list[str],
    model: type[Model],
) -> None:
    """
    Validate the searchable fields of an index. If the searchable fields are not a list,
    it should be "__all__" to indicate that all fields in the model are searchable.

    Args:
        name (str): Index name.
        searchable_fields (Union[str, list]): Searchable fields.
        model_field_names (list[str]): Model field names.

    Raises:
        InvalidSearchableFieldError: If the searchable fields are not a list or "__all__".
    """
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

        raise InvalidSearchableFieldError(
            f"{name}.searchable_fields must be a list or '__all__'"
        )

    for field in searchable_fields:
        if not hasattr(model, field):
            raise InvalidSearchableFieldError(
                f"{model.__name__} does not have a searchable_field named {field}"
            )


def validate_filterable_fields(
    name: str,
    filterable_fields: Union[str, list],
    model_field_names: list[str],
    model: type[Model],
) -> None:
    """
    Validate the filterable fields of an index. If the filterable fields are not a list,
    it should be "__all__" to indicate that all fields in the model are filterable.

    Args:
        name (str): Index name.
        filterable_fields (Union[str, list]): Filterable fields.
        model_field_names (list[str]): Model field names.

    Raises:
        InvalidFilterableFieldError: If the filterable fields are not a list or "__all__".
    """
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

        raise InvalidFilterableFieldError(
            f"{name}.filterable_fields must be a list or '__all__'"
        )

    for field in filterable_fields:
        if not hasattr(model, field):
            raise InvalidFilterableFieldError(
                f"{model.__name__} does not have a filterable_field named {field}"
            )


def validate_sortable_fields(
    name: str,
    sortable_fields: Union[str, list],
    model_field_names: list[str],
    model: type[Model],
) -> None:
    """
    Validate the sortable fields of an index. If the sortable fields are not a list,
    it should be "__all__" to indicate that all fields in the model are sortable.

    Args:
        name (str): Index name.
        sortable_fields (Union[str, list]): Sortable fields.
        model_field_names (list[str]): Model field names.

    Raises:
        InvalidSortableFieldError: If the sortable fields are not a list or "__all__".
    """
    if not isinstance(sortable_fields, list):
        if isinstance(sortable_fields, str) and sortable_fields == "__all__":
            sortable_fields = model_field_names
        else:
            raise InvalidSortableFieldError(
                f"{name}.sortable_fields must be a list or '__all__'"
            )

        raise InvalidSortableFieldError(
            f"{name}.sortable_fields must be a list or '__all__'"
        )

    for field in sortable_fields:
        if not hasattr(model, field):
            raise InvalidSortableFieldError(
                f"{model.__name__} does not have a filterable_field named {field}"
            )

"""
This module contains the exceptions that can be raised by the library.
The exceptions are used to handle errors that occur during the indexing or searching process.
"""


class MissingRequiredFieldError(Exception):
    """Exception raised when a required field is missing."""


class CreateIndexError(Exception):
    """Exception raised when an index creation error occurs."""


class InvalidIndexNameError(Exception):
    """Exception raised when an invalid index name is provided."""


class InvalidDjangoModelError(Exception):
    """Exception raised when an invalid Django model is provided."""


class InvalidPrimaryKeyError(Exception):
    """Exception raised when an invalid primary key is provided."""


class InvalidSearchableFieldError(Exception):
    """Exception raised when an invalid searchable field is provided."""


class InvalidFilterableFieldError(Exception):
    """Exception raised when an invalid filterable field is provided."""


class InvalidSortableFieldError(Exception):
    """Exception raised when an invalid sortable field is provided."""

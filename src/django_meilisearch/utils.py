"""
This module contains utility functions used in the package.
"""

from django.db.models import DateTimeField


def exists_field_in_namespace(field: str, namespace: dict) -> bool:
    """Check if a field exists in a namespace

    Args:
        field (str): The name of the field to check
        namespace (dict): The namespace to check the field

    Returns:
        bool: True if the field exists in the namespace, False otherwise
    """
    father, *children = field.split("__")
    if father not in namespace:
        return False

    if children:
        return exists_field_in_namespace(
            "__".join(children), namespace[father].__dict__
        )

    return True


def get_datetime_fields(model):
    """
    Get the datetime fields from the model based on the namespace.

    Args:
        namespace (dict): The namespace containing the index configuration.
        model (Model): The Django model class.
        model_field_names (list[str]): List of field names in the model.

    Returns:
        list[str]: List of datetime field names.
    """
    model_field_names = [field.name for field in model._meta.fields]

    datetime_fields = []
    for field_name in model_field_names:
        field_class = getattr(model, field_name)
        if isinstance(field_class.field, DateTimeField):
            datetime_fields.append(field_name)

    return datetime_fields

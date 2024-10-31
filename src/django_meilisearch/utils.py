"""
This module contains utility functions used in the package.
"""


def exists_field_in_namespace(field: str, namespace: dict) -> bool:
    """Check if a field exists in a namespace

    Args:
        field (str): The name of the field to check
        namespace (dict): The namespace to check the field

    Returns:
        bool: True if the field exists in the namespace, False otherwise
    """
    father, *children = field.split("__")
    if father not in namespace or not namespace[father]:
        return False

    if children:
        return exists_field_in_namespace(
            "__".join(children), namespace[father].__dict__
        )

    return True

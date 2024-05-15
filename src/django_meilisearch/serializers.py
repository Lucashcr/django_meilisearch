from datetime import datetime


def serialize_field(value):
    """
    Serialize a field value.
    """
    if isinstance(value, datetime):
        return value.timestamp()
    return value


def serialize_queryset(queryset, model):
    """
    Serialize a queryset to a list of dictionaries.
    """
    return [
        {
            field.name: serialize_field(getattr(instance, field.name))
            for field in model._meta.fields
        }
        for instance in queryset
    ]
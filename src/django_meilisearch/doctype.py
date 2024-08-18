from django.db.models import Model
from djantic import ModelSchema
from pydantic import ConfigDict

from django_meilisearch.exceptions import InvalidDjangoModelError, InvalidFilterableFieldError, InvalidIndexNameError, InvalidPrimaryKeyError, InvalidSearchableFieldError, InvalidSortableFieldError, MissingRequiredFieldError
from django_meilisearch.utils import exists_field_in_namespace


class DocType(type):
    __REQUIRED_FIELDS__ = [
        "name",
        "model",
    ]

    REGISTERED_INDEXES = {}

    def __new__(cls, name: str, bases: tuple, namespace: dict):
        if name != "Document":
            if any(
                not exists_field_in_namespace(field, namespace)
                for field in DocType.__REQUIRED_FIELDS__
            ):
                raise MissingRequiredFieldError(f"{name} must have at least {DocType.__REQUIRED_FIELDS__} fields")

            model = namespace["model"]
            
            model_field_names = [field.name for field in model._meta.fields]
            searchable_fields = namespace.get(
                "searchable_fields", model_field_names
            )
            
            filterable_fields = namespace.get(
                "filterable_fields", model_field_names
            )
            
            sortable_fields = namespace.get(
                "sortable_fields", model_field_names
            )
            
            if not isinstance(namespace["name"], str):
                raise InvalidIndexNameError(f"{name}.name must be a string")

            if not issubclass(model, Model):
                raise InvalidDjangoModelError(f"{name}.model must be a Django Model")
            
            cls.primary_key_field = getattr(namespace, "primary_key_field", model._meta.pk.name)
            
            if not isinstance(cls.primary_key_field, str):
                raise InvalidPrimaryKeyError(f"{name}.Django.primary_key_field must be a string")
            if not hasattr(model, cls.primary_key_field):
                raise InvalidPrimaryKeyError(f"{model.__name__} does not have a primary_key_field named {cls.primary_key_field}")

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

                raise InvalidSearchableFieldError(f"{name}.searchable_fields must be a list or '__all__'")

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
                
                raise InvalidFilterableFieldError(f"{name}.filterable_fields must be a list or '__all__'")

            if not isinstance(sortable_fields, list):
                if (
                    isinstance(sortable_fields, str)
                    and sortable_fields == "__all__"
                ):
                    sortable_fields = model_field_names
                else:
                    raise InvalidSortableFieldError(
                        f"{name}.sortable_fields must be a list or '__all__'"
                    )
                
                raise InvalidSortableFieldError(f"{name}.sortable_fields must be a list or '__all__'")

            for field in searchable_fields:
                if not hasattr(model, field):
                    raise InvalidSearchableFieldError(
                        f"{model.__name__} does not have a searchable_field named {field}"
                    )

            for field in filterable_fields:
                if not hasattr(model, field):
                    raise InvalidFilterableFieldError(
                        f"{model.__name__} does not have a filterable_field named {field}"
                    )
            
            for field in sortable_fields:
                if not hasattr(model, field):
                    raise InvalidSortableFieldError(
                        f"{model.__name__} does not have a filterable_field named {field}"
                    )

            cls.searchable_fields = searchable_fields
            cls.filterable_fields = filterable_fields
            cls.sortable_fields = sortable_fields
                        
            cls.schema = type(
                f"{name}Schema",
                (ModelSchema,),
                {
                    "model_config": ConfigDict(
                        model=model,
                    )
                }
            )
            
            index_label = f"{namespace['model']._meta.app_label}.{namespace['__qualname__']}"
            cls.REGISTERED_INDEXES[index_label] = super().__new__(cls, name, bases, namespace)
            return cls.REGISTERED_INDEXES[index_label]

        return super().__new__(cls, name, bases, namespace)

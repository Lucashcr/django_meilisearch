def exists_field_in_namespace(field: str, namespace: dict) -> bool:
    father, *children = field.split("__")
    if father not in namespace:
        return False

    if children:
        return exists_field_in_namespace(
            "__".join(children), namespace[father].__dict__
        )

    return True


def convert_to_camel_case(string: str) -> str:
    if "_" not in string:
        return string.lower()

    splitted = string.split("_")
    return splitted[0] + "".join(word.capitalize() for word in splitted[1:])

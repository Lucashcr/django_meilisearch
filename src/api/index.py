from django_meilisearch.index import BaseIndex

from api.models import Post


class PostIndex(BaseIndex):
    name = "posts"
    model = Post
    # primary_key_field = "id"        # (default is models pk field)
    # searchable_fields = [...]       # (default is all fields in model)
    # filterable_fields = [...]       # (default is all fields in model)
    # sortable_fields = [...]         # (default is all fields in model)

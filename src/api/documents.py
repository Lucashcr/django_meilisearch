from django_meilisearch.documents import Document

from api.models import Post


class PostIndex(Document):
    name = "posts"
    model = Post
    # primary_key_field = "id"        # (default is models pk field) 
    # searchable_fields = [...]   # (default is all fields in model)
    # filterable_fields = [...]       # (default is all fields in model)


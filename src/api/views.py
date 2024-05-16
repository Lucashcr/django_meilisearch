from datetime import datetime
from django.http import JsonResponse

from api.documents import PostIndex
from meilisearchdsl import Q


# Create your views here.
def test_search(request):
    print(datetime.fromtimestamp(1715738200))
    response = PostIndex.search(
        request.GET.get("q"),
        Q(created_at__lte=datetime.fromisoformat("2024-05-15T01:56:40").timestamp()),
        attributes_to_retrieve=["title", "content"],
        attributes_to_highlight=["content"],
    )
    return JsonResponse(response)
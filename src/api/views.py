from django.http import JsonResponse

from api.documents import PostIndex


# Create your views here.
def test_search(request):
    response = PostIndex.search(
        request.GET.get("q"),
        attributes_to_retrieve=["title", "content"],
        attributes_to_highlight=["content"],
        limit=1,
    )
    return JsonResponse(response)

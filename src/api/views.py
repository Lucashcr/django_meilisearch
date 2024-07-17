from django.http import JsonResponse

from api.documents import PostIndex


# Create your views here.
def test_search(request):
    response, status_code = PostIndex.search(
        request.GET.get("q"),
        attributes_to_retrieve=["title", "content"],
        # attributes_to_highlight=["content"],
        sort=["created_at:desc"],
    )

    return JsonResponse(response, status=status_code)

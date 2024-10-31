"""
Views definition for the api app.
"""

from django.http import JsonResponse, HttpRequest

from api.indexes import PostIndex


# Create your views here.
def test_search(request: HttpRequest) -> JsonResponse:
    """This view is used to test the search functionality.

    Args:
        request (django.http.HttpRequest): HTTP request object.

    Returns:
        response (django.http.JsonResponse): HTTP response object.
    """
    response = PostIndex.search(
        request.GET.get("q"),
        # to_queryset=True,
        # attributes_to_retrieve=["title", "content"],
        # attributes_to_highlight=["content"],
        sort=["created_at:desc"],
    )

    return JsonResponse(response)

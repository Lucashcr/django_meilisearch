from django.urls import path

from .views import test_search


urlpatterns = [
    path("test-search/", test_search),
]

# Basic usage

This tutorial will guide you through the basic usage of the `django_meilisearch` library. You will learn how to install the library, configure Meilisearch in your Django project, create a Meilisearch index from a Django model, synchronize data, and perform a basic search.

## Installation and configuration

Install the library in your Django project using your preferred package manager. For example, using `pip`:

```bash
pip install django_meilisearch
```

### Add library to INSTALLED_APPS

To use the library, it's necessary to add it to the `INSTALLED_APPS` list in your Django project's `settings.py` file.

```python
INSTALLED_APPS = [
    ...
    'django_meilisearch',
]
```

### Configure Meilisearch in `settings.py`

Add the following configuration to your Django project's `settings.py` file to connect to your Meilisearch server:

```python
DJANGO_MEILISEARCH = {
    "url": "http://localhost:7700",  # Your MeiliSearch host
    "api_key": "meilisearch_master_key",  # Your MeiliSearch master key
    "timeout": 1,  # Timeout for MeiliSearch requests in seconds (optional)
}
```

## Create a Meilisearch index from a Django model

To create a Meilisearch index from a Django model, you need to define a index class that inherits from `BaseIndex` and specify the model to index.

```python
from django_meilisearch.index import BaseIndex

from myapp.models import MyModel


class MyIndex(BaseIndex):
    name = "my_index"  # Name of the Meilisearch index
    model = MyModel  # Django model to index
```

## How to synchronize data

To synchronize data between your Django model and the Meilisearch index, the library provides management commands to synchronize data between your Django model and the Meilisearch index. They have the following common syntax:

```bash
python manage.py meilisearch {action} {index_name} 
```

The `index_name` parameter is the name of the Meilisearch index to synchronize. If you don't specify an index name, the library will try to apply the `action` synchronize all indexes.

The `action` parameter can be one of the following:

| Action | Description |
| --- | --- |
| `create` | Create the Meilisearch index, if it doesn't exist. Otherwise, it will do nothing. |
| `populate` | Populate an existing Meilisearch index with data from the Django model. If the index doesn't exist, it will return an error. |
| `rebuild` | Destroy the Meilisearch index, recreate it, and populate it with data from the Django model. |
| `destroy` | Clean and destroy the Meilisearch index. |

The actions listed above are synchronous, meaning that they will block the execution of the command until the operation is completed. If you have a large dataset, consider using the asynchronous versions of these commands, which are preffixed with `a`. For example, `apopulate` will populate the index asynchronously.

!!! note
    The asynchronous versions of the commands will return a task ID (or a list of task IDs if you are populating a large dataset) that you can use to check the status of the operation.

## Basic search example

To perform a basic search using the Meilisearch index, you can use the `search` method provided by the index class. The `search` method accepts a query string and returns a list of search results.

```python
from myapp.indexes import MyIndex


class MyView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        results = MyIndex.search(query)
        return JsonResponse({"results": results})
```

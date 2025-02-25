# Advanced features

The integration provide some advanced features in search and indexing. Some of them are about the search index configuration, others are about the search query configuration.

## Index configuration

One of the most important features of the integration is the ability to configure the search index. This is done by adding some variables to the index class. You can configure the primary key field for the index and the fields that should be indexed and fields that should be configured as searchable, filterable or sortable. It's import to optimize the index configuration to improve the search performance, reduce the index size and improve the search relevance.

### Primary key field

The primary key field is the field that uniquely identifies a record in the index. By default, the primary key field is the model primary key field. You can change the primary key field by setting the `primary_key` variable in the index class as long as the field is setted as `unique` in the model.

```python
class MyModelIndex(BaseIndex):
    name = 'my_index'
    model = MyModel
    primary_key = 'my_field'
```

### Searchable fields

The searchable fields are the fields that are used to perform the search. By default, all of the model fields are searchable. You can change the searchable fields by setting the `searchable_fields` variable in the index class to a list of field names.

```python
class MyModelIndex(BaseIndex):
    name = 'my_index'
    model = MyModel
    searchable_fields = ['field1', 'field2']
```

### Filterable fields

The filterable fields are the fields that can be used to filter the search results. By default, all of the model fields are filterable. You can change the filterable fields by setting the `filterable_fields` variable in the index class to a list of field names.

```python
class MyModelIndex(BaseIndex):
    name = 'my_index'
    model = MyModel
    filterable_fields = ['field1', 'field2']
```

### Sortable fields

The sortable fields are the fields that can be used to sort the search results. By default, all of the model fields are sortable. You can change the sortable fields by setting the `sortable_fields` variable in the index class to a list of field names.

```python
class MyModelIndex(BaseIndex):
    name = 'my_index'
    model = MyModel
    sortable_fields = ['field1', 'field2']
```

### Use timestamp

If you want to store the DateTimeField fields as timestamps in the index, you can set the `use_timestamp` variable in the index class to `True`. By default, the DateTimeField fields are stored as strings in the index, but you can store them as timestamps to improve features like sorting and filtering.

```python
class MyModelIndex(BaseIndex):
    name = 'my_index'
    model = MyModel
    use_timestamp = True
```

### Indexing batch size

When you have a large model, with a lot of fields and records, it is recommended to use the indexing batch size to reduce the memory usage and improve the indexing performance. You can change the indexing batch size by setting the `indexing_batch_size` variable in the index class to an integer value. The default value is `100.000` records.

```python
class MyModelIndex(BaseIndex):
    name = 'my_index'
    model = MyModel
    indexing_batch_size = 1_000
```

!!! note
    Make sure to rebuild the index after changing the index configuration to apply the changes.

## Query configuration

In addition to configuring indexes, you can also send some parameters to the search query. These parameters can be used to configure the search query to improve the search relevance, filter the search results, sort the search results, paginate the search results and more.

### Pagination

The pagination parameters are used to paginate the search results. You can paginate the search results by specifying the `offset` and `limit` parameters or the `hits_per_page` and `page` parameters.

#### Offset and limit

Using the `offset` and `limit` parameters you can specify the pagination of the search results similar to the SQL `LIMIT` and `OFFSET` clauses. The `offset` parameter is used to specify the number of records to skip and the `limit` parameter is used to specify the number of records to return.

```python
query = MyIndex.search('python', offset=10, limit=10)
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "published_at": 1672531200
        },
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "published_at": 1672617600
        },
        ...
    ],
    "limit": 10,
    "offset": 10,
    "nbHits": 53
}
```

#### Hits per page and page

Using the `hits_per_page` and `page` parameters you can specify another way to paginate the search results. The `hits_per_page` parameter is used to specify the number of records to return per page and the `page` parameter is used to specify the page number to return.

```python
query = MyIndex.search('python', hits_per_page=10, page=2)
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "published_at": 1672531200
        },
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "published_at": 1672617600
        },
        ...
    ],
    "hits_per_page": 10,
    "page": 2,
    "nbHits": 53
}
```

### Filter

The filter parameter is used to filter the search results. You can filter the search results by specifying one or more fields and values to filter by. It is also possible to use boolean and logical operators to combine multiple filters.

```python
query = MyIndex.search('python', filters='published_at >= 1672617600')
```

Results:

```json
{
    "hits": [
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "published_at": 1672617600
        },
        ...
    ]
}
```

### Facets

The facets parameter is used to retrieve the search results with the facets. You can specify the fields to retrieve the facets by a list of field names.

```python
query = MyIndex.search('python', facets=['genre'])  # ["*"] can be used to retrieve all fields
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "genre": "Programming",
            "published_at": 1672531200
        },
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "genre": "Programming",
            "published_at": 1672617600
        },
        ...
    ],
    "facets": {
        "genre": {
            "Programming": 2
        }
    }
}
```

### Attributes to retrieve

The attributes to retrieve parameter is used to specify the fields to retrieve in the search results. You can specify the fields to retrieve by a list of field names.

```python
query = MyIndex.search('python', attributes_to_retrieve=['title', 'author'])  # ["*"] can be used to retrieve all fields
```

Results:

```json
{
    "hits": [
        {
            "title": "Python Crash Course",
            "author": "Eric Matthes"
        },
        {
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart"
        }
    ]
}
```

### Attributes to crop

The attributes to crop parameter is used to specify the fields to crop in the search results if the field is a text field. You can specify the fields to crop by a list of field names.

```python
query = MyIndex.search('python', attributes_to_crop=['description'])
```

Results:

```json
{
    "hits": [
        {
            "id": 3,
            "title": "Fluent Python",
            "author": "Luciano Ramalho",
            "description": "Python is a powerful programming language that is easy to learn and use.",
            "_formatted": {
                "description": "...a powerful programming language that is easy to learn and use..."
            }
        }
    ]
}
```

#### Crop length

The crop length parameter is used with the `attributes_to_crop` parameter to specify the length of the cropped text.

```python
query = MyIndex.search('python', attributes_to_crop=['description:5'])
```

or

```python
query = MyIndex.search('python', attributes_to_crop=['description'], crop_length=5)
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "description": "In this comprehensive guide, you will learn the fundamentals of programming in Python and develop robust applications with ease.",
            "_formatted": {
                "description": "...programming in Python and develop..."
            }
        }
        ...
    ]
}
```

#### Crop marker

The crop marker parameter is used with the `attributes_to_crop` parameter to specify the marker to use to wrap the cropped text. The default value is `...`.

```python
query = MyIndex.search('python', attributes_to_crop=['description'], crop_marker='[...]')
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "description": "In this comprehensive guide, you will learn the fundamentals of programming in Python and develop robust applications with ease.",
            "_formatted": {
                "description": "[...]the fundamentals of programming in Python and develop robust applications[...]"
            }
        },
        ...
    ]
}
```

### Attributes to highlight

The attributes to highlight parameter is used to specify the fields to highlight in the search results if the field is a text field. You can specify the fields to highlight by a list of field names.

```python
query = MyIndex.search('python', attributes_to_highlight=['title'])
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "description": "In this comprehensive guide, you will learn the fundamentals of programming in Python and develop robust applications with ease.",
            "_formatted": {
                "title": "<em>Python</em> Crash Course"
            }
        },
        ...
    ]
}
```

#### Highlight pre and post tags

It can be used with the `attributes_to_highlight` parameter to specify the tags to use to wrap the highlighted text. The default value is `<em>`.

```python
query = MyIndex.search('python', attributes_to_highlight=['title'], highlight_pre_tag='<strong>', highlight_post_tag='</strong>')
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "description": "In this comprehensive guide, you will learn the fundamentals of programming in Python and develop robust applications with ease.",
            "_formatted": {
                "title": "<strong>Python</strong> Crash Course"
            }
        },
        ...
    ]
}
```

### Show matches position

It is a boolean value used to specify whether to show the matches position in the search results. The default value is `false`.

```python
query = MyIndex.search('python', show_matches_position=True)
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "description": "In this comprehensive guide, you will learn the fundamentals of programming in Python and develop robust applications with ease.",
            "_matchesInfo": {
                "title": [
                    {
                        "start": 0,
                        "length": 6
                    }
                ],
                "description": [
                    {
                        "start": 79,
                        "length": 6
                    }
                ]
            }
        },
        ...
    ]
}
```

### Sort

You can sort the search results by specifying the `sort` parameter. You can specify the fields to sort by and the sort order. The sort order can be `asc` for ascending order or `desc` for descending order.

```python
query = MyIndex.search('python', sort=['published_at:desc'])
```

Results:

```json
{
    "hits": [
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "published_at": 1672617600
        },
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "published_at": 1672531200
        },
        ...
    ]
}
```

### Matching strategy

The matching strategy parameter is used to specify the strategy to use to match the search query. It can be `last`, `all` or `frequency`. The default value is `last`. See the [Meilisearch documentation](https://www.meilisearch.com/docs/reference/api/search#matching-strategy) for more information.

```python
query = MyIndex.search('python', matching_strategy='all')
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "description": "In this comprehensive guide, you will learn the fundamentals of programming in Python and develop robust applications with ease."
        },
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "description": "If you've ever spent hours renaming files or updating hundreds of spreadsheet cells, you know how tedious tasks like these can be. But what if you could have your computer do them for you?"
        },
        ...
    ]
}
```

### Show ranking score

It is a boolean value used to specify whether to show the ranking score in the search results. The default value is `false`.

```python
query = MyIndex.search('python', show_ranking_score=True)
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "_rankingScore": 0.98
        },
        ...
    ]
}
```

### Show ranking score details

It is a boolean value used to specify whether to show the ranking score details in the search results. The default value is `false`. The ranking score details include the number of typos, words, proximity distance, attribute, exact words, exact words distance, words distance, filters, words position, words proximity, attribute score, and custom ranking.

```python
query = MyIndex.search('python', show_ranking_score_details=True)
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "description": "In this comprehensive guide, you will learn the fundamentals of programming in Python and develop robust applications with ease.",
            "_rankingScoreDetails": {
                "words": {
                    "order": 0,
                    "matchingWords": 4,
                    "maxMatchingWords": 4,
                    "score": 1.0
                },
                "typo": {
                    "order": 2,
                    "typoCount": 1,
                    "maxTypoCount": 4,
                    "score": 0.75
                },
                "name:asc": {
                    "order": 1,
                    "value": "python"
                }
            }
        },
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "description": "If you've ever spent hours renaming files or updating hundreds of spreadsheet cells, you know how tedious tasks like these can be. But what if you could have your computer do them for you?",
            "_rankingScoreDetails": {
                "words": {
                    "order": 0,
                    "matchingWords": 4,
                    "maxMatchingWords": 4,
                    "score": 1.0
                },
                "typo": {
                    "order": 2,
                    "typoCount": 1,
                    "maxTypoCount": 4,
                    "score": 0.75
                },
                "name:asc": {
                    "order": 1,
                    "value": "python"
                }
            }
        },
        ...
    ]
}
```

### Ranking score threshold

The ranking score threshold parameter is used to specify the threshold to use to filter the search results by the ranking score excluding the results with a ranking score below the threshold. The default value is `null`.

```python
query = MyIndex.search('python', ranking_score_threshold=0.80)
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "_rankingScore": 0.97
        },
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "_rankingScore": 0.95
        },
        ...
    ]
}
```

### Attributes to search on

The attributes to search on parameter is used to specify the fields to search on in the search query. You can specify the fields to search on by a list of field names.

```python
query = MyIndex.search('python', attributes_to_search_on=['title'])
```

Results:

```json
{
    "hits": [
        {
            "id": 1,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "description": "In this comprehensive guide, you will learn the fundamentals of programming in Python and develop robust applications with ease."
        },
        {
            "id": 2,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "description": "If you've ever spent hours renaming files or updating hundreds of spreadsheet cells, you know how tedious tasks like these can be. But what if you could have your computer do them for you?"
        },
        ...
    ]
}
```

!!! note
    You can find more information about the filter syntax in the [Meilisearch documentation](https://www.meilisearch.com/docs/learn/filtering_and_sorting/filter_search_results).

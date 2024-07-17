from typing import TypedDict

class OptParams(TypedDict):
    offset: int
    limit: int
    hits_per_page: int
    page: int
    filter: str | list
    facets: list[str]
    attributtes_to_retrieve: list[str]
    attributes_to_highlight: list[str]
    crop_length: int
    crop_marker: str
    attributes_to_highlight: list[str]
    highlight_pre_tag: str
    highlight_post_tag: str
    show_matches_position: bool
    sort: list[str]
    matching_strategy: str
    show_ranking_score: bool
    show_ranking_score_details: bool
    ranking_score_threshold: float
    attributes_to_search_on: list[str]
    hybrid: dict
    vector: list[float]
    retrieve_vectors: bool
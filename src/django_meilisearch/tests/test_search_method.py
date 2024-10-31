"""
Test cases for the CLI actions.
"""

from django.test import TestCase

from api.indexes import PostIndex


# Create your tests here.
class TestInitialize(TestCase):
    """
    Test cases for the CLI actions.
    """

    fixtures = ["posts.json"]

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test cases.
        """
        PostIndex.create()
        PostIndex.populate()

    def test_successful_search(self):
        """
        Test the success of the search without any options.
        """
        results = PostIndex.search("itaque")

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["offset"], 0)
        self.assertEqual(results["limit"], 20)
        self.assertEqual(results["estimatedTotalHits"], 7)

    def test_successful_search_with_limit(self):
        """
        Test the success of the search with limit option.
        """
        results = PostIndex.search("itaque", limit=5)

        self.assertEqual(len(results["hits"]), 5)
        self.assertEqual(results["offset"], 0)
        self.assertEqual(results["limit"], 5)
        self.assertEqual(results["estimatedTotalHits"], 7)

    def test_successful_search_with_limit_and_offset(self):
        """
        Test the success of the search with limit and offset options.
        """
        results = PostIndex.search("itaque", limit=5, offset=5)

        self.assertEqual(len(results["hits"]), 2)
        self.assertEqual(results["offset"], 5)
        self.assertEqual(results["limit"], 5)
        self.assertEqual(results["estimatedTotalHits"], 7)

    def test_successful_search_with_hits_per_page(self):
        """
        Test the success of the search with hits per page option.
        """
        results = PostIndex.search("itaque", hits_per_page=5)

        self.assertEqual(len(results["hits"]), 5)
        self.assertEqual(results["page"], 1)
        self.assertEqual(results["hitsPerPage"], 5)
        self.assertEqual(results["totalPages"], 2)
        self.assertEqual(results["totalHits"], 7)

    def test_successful_search_with_hits_per_page_and_page(self):
        """
        Test the success of the search with hits per page and page options.
        """
        results = PostIndex.search("itaque", hits_per_page=5, page=2)

        self.assertEqual(len(results["hits"]), 2)
        self.assertEqual(results["page"], 2)
        self.assertEqual(results["hitsPerPage"], 5)
        self.assertEqual(results["totalPages"], 2)
        self.assertEqual(results["totalHits"], 7)

    def test_successful_search_with_str_filter(self):
        """
        Test the success of the search with string filter option.
        """
        results = PostIndex.search("itaque", filter="id > 34 AND id < 37 OR id = 48")

        self.assertEqual(len(results["hits"]), 2)
        self.assertEqual(results["estimatedTotalHits"], 2)

    def test_successful_search_with_list_filter_and(self):
        """
        Test  the success of the search with list filter and option.
        """
        results = PostIndex.search("itaque", filter=["id > 34", "id < 37"])

        self.assertEqual(len(results["hits"]), 1)
        self.assertEqual(results["estimatedTotalHits"], 1)

    def test_successful_search_with_list_filter_or(self):
        """
        Test  the success of the search with filter list or option.
        """
        results = PostIndex.search("itaque", filter=[["id = 36", "id = 48"]])

        self.assertEqual(len(results["hits"]), 2)
        self.assertEqual(results["estimatedTotalHits"], 2)

    def test_successful_search_with_facets(self):
        """
        Test the success of the search with facets option.
        """
        results = PostIndex.search("itaque", facets=["id"])

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertEqual(
            results["facetDistribution"],
            {"id": {"12": 1, "18": 1, "21": 1, "34": 1, "36": 1, "44": 1, "48": 1}},
        )
        self.assertEqual(
            results["facetStats"],
            {
                "id": {
                    "min": 12,
                    "max": 48,
                }
            },
        )

    def test_successful_search_with_attributes_to_retrieve(self):
        """
        Test the success of the search with attributes to retrieve option.
        """
        results = PostIndex.search("itaque", attributes_to_retrieve=["id", "title"])

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(all("id" in hit and "title" in hit for hit in results["hits"]))
        self.assertTrue(
            all(
                "content" not in hit and "create_at" not in hit
                for hit in results["hits"]
            )
        )

    def test_successful_search_with_attributes_to_crop(self):
        """
        Test the success of the search with attributes to crop option.
        """
        results = PostIndex.search("itaque", attributes_to_crop=["content"])

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(
            (
                len(hit["_formatted"]["content"].split(" ")) <= 10
                for hit in results["hits"]
            )
        )

    def test_successful_search_with_crop_length(self):
        """
        Test the success of the search with crop length option.
        """
        results = PostIndex.search(
            "itaque", attributes_to_crop=["content"], crop_length=5
        )

        import json

        print(json.dumps(results, indent=4))

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(
            (
                len(hit["_formatted"]["content"].split(" ")) <= 5
                for hit in results["hits"]
            )
        )

    def test_successful_search_with_crop_marker(self):
        """
        Test the success of the search with crop marker option.
        """
        results = PostIndex.search(
            "itaque", attributes_to_crop=["content"], crop_marker="..."
        )

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(
            any("..." in hit["_formatted"]["content"] for hit in results["hits"])
        )
        self.assertTrue(
            all("\u2026" not in hit["_formatted"]["content"] for hit in results["hits"])
        )

    def test_successful_search_with_attributes_to_search_on(self):
        """
        Test the success of the search with attributes to search on option.
        """
        results = PostIndex.search("itaque", attributes_to_search_on=["title"])

        self.assertEqual(len(results["hits"]), 3)
        self.assertEqual(results["estimatedTotalHits"], 3)
        self.assertTrue(all("itaque" in hit["title"] for hit in results["hits"]))

    def test_successful_search_with_attributes_to_highlight(self):
        """
        Test the success of the search with attributes to highlight option.
        """
        results = PostIndex.search("itaque", attributes_to_highlight=["title"])

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(
            any("<em>" in hit["_formatted"]["title"] for hit in results["hits"])
        )
        self.assertTrue(
            all("<em>" not in hit["_formatted"]["content"] for hit in results["hits"])
        )

    def test_successful_search_with_highlight_pre_tag(self):
        """
        Test the success of the search with highlight pre tag option.
        """
        results = PostIndex.search(
            "itaque", attributes_to_highlight=["content"], highlight_pre_tag="<strong>"
        )

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(
            any("<strong>" in hit["_formatted"]["content"] for hit in results["hits"])
        )
        self.assertTrue(
            all("<strong>" not in hit["_formatted"]["title"] for hit in results["hits"])
        )

    def test_successful_search_with_highlight_post_tag(self):
        """
        Test the success of the search with highlight post tag option.
        """
        results = PostIndex.search(
            "itaque",
            attributes_to_highlight=["content"],
            highlight_post_tag="</strong>",
        )

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(
            any("</strong>" in hit["_formatted"]["content"] for hit in results["hits"])
        )
        self.assertTrue(
            all(
                "</strong>" not in hit["_formatted"]["title"] for hit in results["hits"]
            )
        )

    def test_successful_search_with_show_matches_position(self):
        """
        Test the success of the search with show matches position option.
        """
        results = PostIndex.search("itaque", show_matches_position=True)

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(all("_matchesPosition" in hit for hit in results["hits"]))

    def test_successful_search_with_sorted_asc(self):
        """
        Test the success of the search with sort option.
        """
        results = PostIndex.search("", sort=["created_at:asc"])

        import json

        print(json.dumps(results, indent=4))

        self.assertEqual(len(results["hits"]), 20)
        self.assertEqual(results["estimatedTotalHits"], 50)

        created_at_list = [hit["created_at"] for hit in results["hits"]]
        self.assertEqual(created_at_list, sorted(created_at_list))

    def test_successful_search_with_sorted_desc(self):
        """
        Test the success of the search with sort option.
        """
        results = PostIndex.search("", sort=["created_at:desc"])

        self.assertEqual(len(results["hits"]), 20)
        self.assertEqual(results["estimatedTotalHits"], 50)

        created_at_list = [hit["created_at"] for hit in results["hits"]]
        self.assertEqual(created_at_list, sorted(created_at_list, reverse=True))

    def test_success_search_with_last_matching_strategy(self):
        """
        Test the success of the search with matching strategy option.
        """
        results = PostIndex.search("dolor itaque", matching_strategy="last")

        self.assertEqual(len(results["hits"]), 14)
        self.assertEqual(results["estimatedTotalHits"], 14)

        id_list = [hit["id"] for hit in results["hits"]]
        self.assertEqual(id_list, [18, 44, 34, 21, 22, 30, 2, 45, 29, 5, 8, 7, 9, 41])

    def test_success_search_with_all_matching_strategy(self):
        """
        Test the success of the search with matching strategy option.
        """
        results = PostIndex.search("dolor itaque", matching_strategy="all")

        self.assertEqual(len(results["hits"]), 4)
        self.assertEqual(results["estimatedTotalHits"], 4)

        id_list = [hit["id"] for hit in results["hits"]]
        self.assertEqual(id_list, [18, 44, 34, 21])

    def test_success_search_with_frequency_matching_strategy(self):
        """
        Test the success of the search with matching strategy option.
        """
        results = PostIndex.search("dolor itaque", matching_strategy="frequency")

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)

        id_list = [hit["id"] for hit in results["hits"]]
        self.assertEqual(sorted(id_list), [12, 18, 21, 34, 36, 44, 48])
    
    def test_success_search_with_no_ranking_score(self):
        """
        Test the success of the search with show ranking score option.
        """
        results = PostIndex.search("itaque", show_ranking_score=False)

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(all("_rankingScore" not in hit for hit in results["hits"]))
    
    def test_success_search_with_ranking_score(self):
        """
        Test the success of the search with show ranking score option.
        """
        results = PostIndex.search("itaque", show_ranking_score=True)

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(all("_rankingScore" in hit for hit in results["hits"]))
    
    def test_success_search_with_no_ranking_score_details(self):
        """
        Test the success of the search with show ranking score details option.
        """
        results = PostIndex.search("itaque", show_ranking_score_details=False)

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(all("_rankingScoreDetails" not in hit for hit in results["hits"]))
    
    def test_success_search_with_ranking_score_details(self):
        """
        Test the success of the search with show ranking score details option.
        """
        results = PostIndex.search("itaque", show_ranking_score_details=True)

        self.assertEqual(len(results["hits"]), 7)
        self.assertEqual(results["estimatedTotalHits"], 7)
        self.assertTrue(all("_rankingScoreDetails" in hit for hit in results["hits"]))
    
    def test_success_search_with_ranking_score_threshold(self):
        """
        Test the success of the search with ranking score threshold option.
        """
        results = PostIndex.search("itaque", ranking_score_threshold=0.75, show_ranking_score=True)

        self.assertEqual(len(results["hits"]), 6)
        self.assertEqual(results["estimatedTotalHits"], 6)
        self.assertTrue(all(hit["_rankingScore"] >= 0.75 for hit in results["hits"]))
        
        id_list = [hit["id"] for hit in results["hits"]]
        self.assertEqual(sorted(id_list), [12, 18, 21, 34, 36, 48])

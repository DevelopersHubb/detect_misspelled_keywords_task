import unittest
from KeywordSuggestionFetcher import (
    is_misspelled,
    find_correct_keyword,
    process_keyword,
)


class TestIsMisspelled(unittest.TestCase):

    def test_is_misspelled_with_empty_suggestions(self):
        keyword = "apple"
        suggestions = []
        result = is_misspelled(keyword, suggestions)
        self.assertTrue(result)

    def test_is_misspelled_with_keyword_in_suggestions(self):
        keyword = "apple"
        suggestions = ["apple", "banana", "cherry"]
        result = is_misspelled(keyword, suggestions)
        self.assertFalse(result)

    def test_is_misspelled_with_short_keyword(self):
        keyword = "a"
        suggestions = ["apple", "banana", "cherry"]
        result = is_misspelled(keyword, suggestions)
        self.assertFalse(result)

    def test_is_misspelled_with_keyword_not_in_suggestions(self):
        keyword = "grape"
        suggestions = ["apple", "banana", "cherry"]
        result = is_misspelled(keyword, suggestions)
        self.assertTrue(result)


class TestFindCorrectKeyword(unittest.TestCase):

    def test_find_correct_keyword_with_empty_suggestions(self):
        keyword = "apple"
        suggestions = []
        result = find_correct_keyword(keyword, suggestions)
        self.assertEqual(result, keyword)

    def test_find_correct_keyword_with_misspelled_keyword(self):
        keyword = "fru"
        suggestions = ["fruit", "apple", "banana", "cherry"]
        result = find_correct_keyword(keyword, suggestions)
        self.assertEqual(result, "fruit")

    def test_find_correct_keyword_with_correct_keyword(self):
        keyword = "apple"
        suggestions = ["apple", "banana", "cherry"]
        result = find_correct_keyword(keyword, suggestions)
        self.assertEqual(result, keyword)


class TestProcessKeyword(unittest.TestCase):

    def test_process_keyword(self):
        keyword = "apple"
        suggestions = ["apple", "banana", "cherry"]
        result = process_keyword((keyword, suggestions))
        self.assertEqual(result, (keyword, suggestions, False, keyword))


if __name__ == '__main__':
    unittest.main()

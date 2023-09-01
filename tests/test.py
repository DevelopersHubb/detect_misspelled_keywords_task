import logging
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp

from KeywordSuggestionFetcher import (fetch_google_suggestions,
                                      fetch_suggestions_async,
                                      find_correct_keyword, is_misspelled,
                                      process_keyword)


class TestFetchGoogleSuggestions(unittest.IsolatedAsyncioTestCase):

    async def test_fetch_google_suggestions_successful(self):
        session_mock = AsyncMock(aiohttp.ClientSession)
        response_mock = MagicMock()
        response_mock.json = AsyncMock(return_value=["python", "python"])

        session_mock.get.return_value.__aenter__.return_value = response_mock

        suggestions = await fetch_google_suggestions(session_mock, "python")

        self.assertIn(suggestions, ["python", "python tutorials"])
        url = "http://suggestqueries.google.com/complete/search?client=firefox&q=python"
        session_mock.get.assert_called_once_with(url)

    async def test_fetch_google_suggestions_error(self):
        session_mock = AsyncMock(aiohttp.ClientSession)
        session_mock.get.side_effect = aiohttp.ClientError("Connection Error")

        suggestions = await fetch_google_suggestions(session_mock, "python")

        self.assertEqual(suggestions, [])
        session_mock.get.assert_called_once()


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


class TestFetchSuggestionsAsync(unittest.IsolatedAsyncioTestCase):

    async def test_fetch_suggestions_async_success(self):
        async def mock_fetch_google_suggestions(session, keyword):
            return ["suggestion1", "suggestion2"]

        keyword = "apple"
        session = AsyncMock()

        with patch("KeywordSuggestionFetcher.fetch_google_suggestions", side_effect=mock_fetch_google_suggestions):
            result = await fetch_suggestions_async(keyword, session)

        self.assertEqual(result, (keyword, ["suggestion1", "suggestion2"]))

    async def test_fetch_suggestions_async_exception(self):
        async def mock_fetch_google_suggestions(session, keyword):
            raise Exception("Test Exception")

        keyword = "apple"
        session = AsyncMock()

        with patch("KeywordSuggestionFetcher.fetch_google_suggestions", side_effect=mock_fetch_google_suggestions):
            with self.assertLogs(level=logging.ERROR):
                result = await fetch_suggestions_async(keyword, session)

        self.assertEqual(result, (keyword, []))


if __name__ == '__main__':
    unittest.main()

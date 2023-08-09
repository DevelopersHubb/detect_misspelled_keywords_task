import pytest
from unittest import mock
from KeywordSuggestionFetcher import (
    fetch_google_suggestions,
    is_misspelled,
    find_correct_keyword,
)


@pytest.fixture
def mock_response():
    response_mock = mock.Mock()
    response_mock.json.return_value = ["data", ["suggestion1", "suggestion2"]]
    response_mock.raise_for_status.return_value = None
    return response_mock


@mock.patch("KeywordSuggestionFetcher.requests.get")
def test_fetch_google_suggestions(mock_get, mock_response):
    mock_get.return_value = mock_response
    suggestions = fetch_google_suggestions("test")
    assert suggestions == ["suggestion1", "suggestion2"]


def test_is_misspelled():
    assert is_misspelled("appl", ["apple", "banana"]) is True
    assert is_misspelled("apple", ["apple", "banana"]) is False
    assert is_misspelled("ap", ["apple", "banana"]) is False
    assert is_misspelled("apples", []) is True


def test_find_correct_keyword():
    assert find_correct_keyword("app", ["apple", "banana"]) == "apple"
    assert find_correct_keyword("appl", ["apple", "banana"]) == "apple"
    assert find_correct_keyword("appll", ["apple", "banana"]) == "apple"
    assert find_correct_keyword("banana", []) == "banana"

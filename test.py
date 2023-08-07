import pytest
from detect_misspelled_keywords import (
    fetch_google_suggestions,
    is_misspelled,
    find_correct_keyword,
    fetch_suggestions_async
)


@pytest.fixture
def suggestions_data():
    return ["apple", "orange", "banana", "strawberry"]


@pytest.fixture
def incorrect_keyword():
    return "appel"


@pytest.fixture
def correct_keyword():
    return "apple"


@pytest.fixture
def keyword_with_suggestions():
    return "oran"


@pytest.fixture
def keyword_with_no_suggestions():
    return "apple"


@pytest.mark.asyncio
async def test_fetch_suggestions_async():
    keyword = "orange"
    suggestions_list = []
    await fetch_suggestions_async(keyword, suggestions_list)
    assert "orange" in suggestions_list
    assert len(suggestions_list) > 0


def test_fetch_google_suggestions():
    keyword = "apple"
    suggestions = fetch_google_suggestions(keyword)
    expected_suggestions = {
        "apple", "apple id", "apple id login", "apple watch", "apple id create",
        "apple store", "apple watch series 8", "apple watch price in pakistan",
        "apple cider vinegar", "apple iphone 15"}

    assert expected_suggestions.issubset(set(suggestions))


def test_is_misspelled(incorrect_keyword, correct_keyword, suggestions_data):
    assert is_misspelled(incorrect_keyword, suggestions_data)
    assert not is_misspelled(correct_keyword, suggestions_data)


def test_find_correct_keyword(keyword_with_suggestions, keyword_with_no_suggestions, suggestions_data):
    assert find_correct_keyword(keyword_with_suggestions, suggestions_data) == "apple"
    assert find_correct_keyword(keyword_with_no_suggestions, suggestions_data) == keyword_with_no_suggestions


def test_is_misspelled_empty_suggestions_list():
    keyword = "apple"
    suggestions_data = []
    assert is_misspelled(keyword, suggestions_data)


def test_is_misspelled_greater_distance():
    keyword = "aple"
    suggestions_data = ["apple", "banana"]
    threshold = 1
    assert is_misspelled(keyword, suggestions_data, threshold)


def test_find_correct_keyword_empty_suggestions_list():
    keyword = "apple"
    suggestions_data = []
    assert find_correct_keyword(keyword, suggestions_data) == keyword


if __name__ == "__main__":
    pytest.main()

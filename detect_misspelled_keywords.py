import asyncio
import requests
from billiard import Manager
import json


def fetch_google_suggestions(keyword):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        suggestions = response.json()[1]
        return suggestions
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching suggestions: {e}")
        return []


def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(
                    1 + min((distances[index1], distances[index1 + 1], new_distances[-1]))
                )
        distances = new_distances

    return distances[-1]


def is_misspelled(keyword, suggestions, threshold=2):
    if not suggestions:
        return True

    if keyword in suggestions:
        return False

    if len(keyword) <= 2:
        return False

    for suggestion in suggestions:
        distance = levenshtein_distance(keyword, suggestion)
        if distance <= threshold:
            return True

    return False


def find_correct_keyword(keyword, suggestions):
    if not suggestions:
        return keyword

    return min(suggestions, key=len)


async def fetch_suggestions_async(keyword, suggestions_list):
    try:
        suggestions = fetch_google_suggestions(keyword)
        suggestions_list.extend(suggestions)
    except Exception as e:
        print(f"Error occurred while fetching suggestions asynchronously: {e}")


async def main():
    user_input = input("Search keyword: ")
    keyword = user_input
    manager = Manager()
    suggestions_list = manager.list()
    tasks = []
    tasks.append(fetch_suggestions_async(keyword, suggestions_list))

    await asyncio.gather(*tasks)

    suggestions = list(suggestions_list)
    is_misspelled_result = is_misspelled(keyword, suggestions)
    correct_keyword_result = find_correct_keyword(keyword, suggestions)

    result = {
        "keyword": keyword,
        "suggestions": suggestions,
        "is_misspelled": is_misspelled_result,
        "correct_keyword": correct_keyword_result,
        "reason": None
    }
    result_list = [result]
    print(json.dumps(result_list, indent=1))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

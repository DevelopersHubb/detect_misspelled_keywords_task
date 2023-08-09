import asyncio
import json
import logging
import requests


logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_google_suggestions(keyword):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        suggestions = response.json()[1]
        return suggestions
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching suggestions: {e}")
        return []


def is_misspelled(keyword, suggestions):
    if not suggestions:
        return True

    if keyword in suggestions:
        return False

    if len(keyword) <= 2:
        return False

    return keyword not in suggestions


def find_correct_keyword(keyword, suggestions):
    if not suggestions:
        return keyword

    if is_misspelled(keyword, suggestions):
        return min(suggestions, key=len)
    return keyword


async def fetch_suggestions_async(keyword, suggestions_list):
    try:
        suggestions = fetch_google_suggestions(keyword)
        suggestions_list.append((keyword, suggestions))
    except Exception as e:
        logging.error(f"Error occurred while fetching suggestions asynchronously: {e}")


async def main():
    keywords = input().split()
    suggestions_list = []
    tasks = []

    for keyword in keywords:
        tasks.append(fetch_suggestions_async(keyword, suggestions_list))

    await asyncio.gather(*tasks)

    results = []

    for keyword, suggestions in suggestions_list:
        is_misspelled_result = is_misspelled(keyword, suggestions)
        correct_keyword_result = find_correct_keyword(keyword, suggestions)

        result = {
            "keyword": keyword,
            "suggestions": suggestions,
            "is_misspelled": is_misspelled_result,
            "correct_keyword": correct_keyword_result,
            "reason": None
        }
        results.append(result)

    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

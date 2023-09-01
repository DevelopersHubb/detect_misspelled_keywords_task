import asyncio
import json
import logging
from dataclasses import dataclass

import aiohttp
from billiard import Pool

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


@dataclass
class Result:
    keyword: str
    suggestions: list
    is_misspelled: bool
    correct_keyword: str
    reason: str = None


async def fetch_google_suggestions(session, keyword):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"

    try:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json(content_type="text/javascript")
            suggestions = data[1]
            return suggestions
    except aiohttp.ClientError as e:
        logging.error(f"Error occurred while fetching suggestions at : {e}")
        return []


def is_misspelled(keyword, suggestions):
    if keyword in suggestions or len(keyword) <= 2:
        return False
    return True


def find_correct_keyword(keyword, suggestions):
    if not suggestions:
        return keyword

    if is_misspelled(keyword, suggestions):
        return min(suggestions, key=len)
    return keyword


async def fetch_suggestions_async(keyword, session):
    try:
        suggestions = await fetch_google_suggestions(session, keyword)
        return (keyword, suggestions)
    except Exception as e:
        logging.error(f"Error occurred while fetching suggestions asynchronously: {e}")
        return (keyword, [])


def process_keyword(keyword_suggestions):
    keyword, suggestions = keyword_suggestions
    is_misspelled_result = is_misspelled(keyword, suggestions)
    correct_keyword_result = find_correct_keyword(keyword, suggestions)

    return keyword, suggestions, is_misspelled_result, correct_keyword_result


def main():
    keywords = input().split()
    suggestions_list = []
    final_results = []

    async def run_asyncio():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_suggestions_async(keyword, session) for keyword in keywords]
            results = await asyncio.gather(*tasks)
            for result in results:
                suggestions_list.append(result)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_asyncio())

    pool = Pool()
    results = pool.map(process_keyword, suggestions_list)
    pool.close()
    pool.join()

    for keyword, suggestions, is_misspelled_result, correct_keyword_result in results:
        result = Result(keyword, suggestions, is_misspelled_result, correct_keyword_result)
        final_results.append(result)
    json_data = json.dumps([result.__dict__ for result in final_results], indent=2)
    print(json_data)


if __name__ == "__main__":
    main()

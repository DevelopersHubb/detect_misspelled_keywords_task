import asyncio
import requests
import gtts
import playsound
from billiard import Process, Manager

def fetch_google_suggestions(keyword):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        suggestions = response.json()[1]
        return suggestions
    else:
        return []

def is_misspelled(keyword, suggestions):
    if keyword in suggestions:
        return False

    if len(keyword) <= 2:
        return False

    shortest_suggestion = min(suggestions, key=len)
    keyword_words = keyword.split()
    shortest_suggestion_words = shortest_suggestion.split()

    if len(keyword_words) <= len(shortest_suggestion_words):
        return False

    for i in range(len(shortest_suggestion_words)):
        if keyword_words[i] != shortest_suggestion_words[i]:
            return True

    return False

def find_correct_keyword(keyword, suggestions):
    return min(suggestions, key=len)

async def fetch_suggestions_async(keyword, suggestions_dict):
    suggestions = fetch_google_suggestions(keyword)
    suggestions_dict[keyword] = suggestions

async def main():

    user_input = input("Search keyword: ")
    keyword = user_input 
    
# this is an additional feature here sound is used for google text to speech
    sound = gtts.gTTS(keyword, lang='en')
    sound.save("play.mp3")
    playsound.playsound("play.mp3")
    
    manager = Manager()
    suggestions_dict = manager.dict()

    tasks = []
    tasks.append(fetch_suggestions_async(keyword, suggestions_dict))

    await asyncio.gather(*tasks)

    suggestions = suggestions_dict.get(keyword, [])
    is_misspelled_result = is_misspelled(keyword, suggestions)
    correct_keyword_result = find_correct_keyword(keyword, suggestions)

    result = {
        "keyword": keyword,
        "suggestions": suggestions,
        "is_misspelled": is_misspelled_result,
        "correct_keyword": correct_keyword_result,
        "reason": None
    }

    print(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
# Keyword Suggestion Fetcher

This Python script demonstrates an asynchronous approach to fetching keyword suggestions from Google using the asyncio library. It also includes functionalities to identify misspelled keywords and find correct alternatives.

## Overview
This script fetches keyword suggestions from Google's autocomplete service and performs the following tasks:

<b>Fetching Suggestions:</b> The <b>fetch_google_suggestions</b> function sends a GET request to Google's suggestion API for a given keyword and retrieves a list of suggested completions.

<b>Misspelled Keywords:</b> The <b>is_misspelled</b> function checks whether a keyword is likely misspelled by comparing it with the suggestions. It takes into account the keyword's length and presence in the suggestions list.

<b>Finding Correct Keyword:</b> The <b>find_correct_keyword</b> function determines the correct keyword among the suggestions. If the keyword is identified as misspelled, the function selects the suggestion with the shortest length as the correct keyword.

<b>Asynchronous Fetching:</b> The <b>fetch_suggestions_async</b> function fetches suggestions asynchronously using the asyncio library, enabling concurrent requests and faster execution.

<b>Main Execution:</b> The <b>main</b> coroutine takes a list of keywords as input, initiates asynchronous suggestion fetching tasks, gathers the results, and constructs a JSON report containing keyword, suggestions, misspelled status, correct keyword, and reason for each keyword.

## How to Use
1. Install the required dependencies by running:
'''pip install -r requirements.txt'''
2. Run the script by executing:
'''python KeywordSuggestionFetcher.py'''
Provide a space-separated list of keywords as input.

## Dependencies
<b>asyncio</b>: Python's built-in library for asynchronous programming.
<b>aiohttp</b>: The script uses aiohttp to make asynchronous HTTP requests to Google's suggestion API.
<b>billiard</b>: Python multiprocessing library

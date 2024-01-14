import os
import requests
import random
import time
from dotenv import load_dotenv

# Gets the API key from the environment file
load_dotenv()
API_KEY = os.environ.get("API_KEY")


# Retrieve book summaries from Google Books API
def get_user_book_summaries(isbn_list, user_key=None):
    summaries = []
    book_names = []

    KEY = user_key or API_KEY

    for isbn in isbn_list:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={KEY}"
        response = requests.get(url)
        time.sleep(1)

        if response.status_code == 200:
            data = response.json()

            if "items" in data and len(data["items"]) > 0:
                summary = data["items"][0]["volumeInfo"].get(
                    "description", "No summary available"
                )

                if summary != "No summary available":
                    summaries.append(summary)

                    name = data["items"][0]["volumeInfo"]["title"]
                    book_names.append(name)

    if len(summaries) == 0:
        print(
            "Sorry, none of the user book summaries are valid. Please enter more books."
        )

    return summaries, book_names


def get_other_book_data(
    genre, genre_to_read, user_book_names, user_key=None, max_results=200
):
    KEY = user_key or API_KEY

    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre_to_read}+{genre}&startIndex=0&maxResults=1&key={KEY}"
    response = requests.get(url)
    time.sleep(1)

    data = response.json()
    total_items = data.get("totalItems", 0)
    results = max_results // 5

    unique_books = set(user_book_names)
    book_data = []

    for _ in range(5):
        start_index = random.randint(0, total_items)
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre_to_read}+{genre}&startIndex={start_index}&maxResults={results}&key={KEY}"
        response = requests.get(url)
        time.sleep(1)

        if response.status_code == 200:
            books = response.json().get("items", [])
            for book in books:
                id = book["volumeInfo"].get("title")

                if id in unique_books:
                    continue

                unique_books.add(id)

                book_info = {
                    "title": id,
                    "isbn": book["volumeInfo"]
                    .get("industryIdentifiers", [{}])[0]
                    .get("identifier", "No ISBN available"),
                    "summary": book["volumeInfo"].get(
                        "description", "No summary available"
                    ),
                }
                book_data.append(book_info)
        else:
            print("Failed to fetch data:", response.status_code)

    return book_data

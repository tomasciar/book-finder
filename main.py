import pandas as pd
import numpy as np
from data_processing import get_user_preferences, calculate_similarity
from api import get_user_book_summaries, get_other_book_data


def main():
    df = pd.read_csv("books.csv")

    isbn_list, genre, genre_to_read = get_user_preferences(df)
    print(f"\nSearching for similarities of {isbn_list} in {genre_to_read} and {genre}...\n")

    user_summaries, book_names = get_user_book_summaries(isbn_list)
    other_book_data = get_other_book_data(genre, genre_to_read, book_names)

    similarities = calculate_similarity(user_summaries, other_book_data)
    print(similarities, "\n")

    most_similar_books = np.argsort(similarities)[-3:]
    print("Based on genres and cosine similarity, the recommended books are:\n")
    for index in most_similar_books:
        book = other_book_data[index]
        print(f"Title: {book["title"]}\n")
        print(f"Summary: {book["summary"]}\n")


if __name__ == "__main__":
    main()

import numpy as np
from utils import get_closest_match
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from genres import genres


# Query the user for book preferences
def get_user_preferences(df):
    titles = input(
        "Enter the titles of your favorite books (no punctuation), separated by commas: "
    )
    genre = input("Enter your favorite genre: ")
    genre_to_read = input("Enter the genre you're looking to read: ")

    genre = get_closest_match(genre, genres)[0]
    genre_to_read = get_closest_match(genre_to_read, genres)[0]

    isbn_list = []
    for title in titles.split(","):
        isbn = df[df["title"] == get_closest_match(title, df["title"])[0]]["isbn"]

        if not isbn.empty:
            for id in isbn.values:
                isbn_list.append(id)

    return isbn_list, genre, genre_to_read


def calculate_similarity(user_summaries, other_book_data):
    num_books = len(other_book_data)
    other_summaries = [other_book_data[i]["summary"] for i in range(num_books)]

    # Vectorize the summaries
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(
        np.concatenate((other_summaries, user_summaries), axis=None)
    )

    # Compute the cosine similarity matrix
    # The matrix includes similarities of all books against all others,
    # including the user's books against all other books
    cosine_similarity_matrix = cosine_similarity(tfidf_matrix)

    num_user_books = len(user_summaries)
    num_dataset_books = len(other_summaries)
    similarities = np.zeros(num_dataset_books)

    for i in range(num_dataset_books, num_dataset_books + num_user_books):
        similarities += cosine_similarity_matrix[i, :num_dataset_books]

    return similarities

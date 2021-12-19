from typing import Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import *


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class InvalidYearException(Exception):
    pass


def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException
    return book_to_dict(book)


def get_random_books(quantity, repo: AbstractRepository):
    return repo.get_books_random(quantity)


def get_all_books(repo: AbstractRepository):
    books = repo.get_all_books()
    return books


# Function for getting user's favourite books
def get_users_favourite_books(user_name: str, repo: AbstractRepository):

    # Get User Object with user_name
    user = repo.get_user(user_name)

    # Get User's favourite books in dictionary form (list of book dictionaries)
    users_favourite_books = books_to_dict(user.favourites)

    return users_favourite_books


# Function for adding a book to a user's favorites
def add_book_to_favourites(book_id: int, user_name: str, repo: AbstractRepository):

    # Get User Object with user_name
    user = repo.get_user(user_name)

    # Get Book Object with book_id
    book = repo.get_book(book_id)

    user.add_to_favourites(book)


def get_books_by_author(author: Author, repo: AbstractRepository):
    return books_to_dict(repo.get_books_by_author(author))


def get_books_by_release_year(year, repo: AbstractRepository):
    if not ((isinstance(year, int) and year >= 0) or year is None):
        raise InvalidYearException
    return repo.get_book_release_year(year)


def add_review(
    book_id: int, review_text: str, user_name: str, repo: AbstractRepository
):
    # Check that the book exists.
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    review = make_review(review_text, user, book)
    repo.add_review(review)


def get_review(book_id, repo: AbstractRepository):
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException
    return reviews_to_dict(book.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================


def book_to_dict(book: Book):
    book_dict = {
        "id": book.book_id,
        "release_year": book.release_year,
        "title": book.title,
        "hyperlink": book.hyperlink,
        "image_hyperlink": book.image_hyperlink,
        "reviews": reviews_to_dict(book.reviews),
        "publisher": book.publisher,
        "description": book.description,
        "authors": [author.full_name for author in book.authors],
        "average_rating": book.average_rating,
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(book) for book in books]


def review_to_dict(review: Review):
    review_dict = {
        "user_name": review.user.user_name,
        "book_id": review.book.book_id,
        "review_text": review.review_text,
        "timestamp": review.timestamp,
        "user": review.user,
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]

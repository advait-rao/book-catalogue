from typing import Iterable
import random

from library.adapters.repository import AbstractRepository
from library.domain.model import *
from library.adapters.repository import AbstractRepository


def get_all_release_years(repo: AbstractRepository):
    return repo.get_all_release_years()


def get_all_books(repo: AbstractRepository):
    return repo.get_all_books()


def get_all_authors(repo: AbstractRepository):
    return repo.get_all_authors()


def get_all_publishers(repo: AbstractRepository):
    return repo.get_publishers()


def get_publisher_name(publisher_name: str, repo: AbstractRepository):
    return repo.get_publisher_by_name(publisher_name)


def get_publisher_books(publisher: Publisher, repo: AbstractRepository):
    return repo.get_books_by_publisher(publisher)


def get_books_by_publisher_name(publisher_name: str, repo: AbstractRepository):
    publisher = get_publisher_name(publisher_name, repo)
    return get_publisher_books(publisher, repo)


def get_book_author(author: Author, repo: AbstractRepository):
    return repo.get_books_by_author(author)


def get_books_by_author_name(author_name: str, repo: AbstractRepository):
    all_authors = get_all_authors(repo)
    for author in all_authors:
        if author.full_name == author_name:
            return get_book_author(author, repo)
    return None

    return get_book_author(author, repo)


def get_authors_name(name: str, repo: AbstractRepository):
    return repo.find_authors_by_name(name)


def get_author_id(id: int, repo: AbstractRepository):
    return repo.get_author_by_id(id)


def get_books_random(quantity, repo: AbstractRepository):
    books = repo.get_books_random(quantity)

    return books_to_dict(books)


# ============================================
# Functions to convert dicts to model entities
# ============================================
def book_to_dict(book: Book):
    book_dict = {
        "id": book.book_id,
        "release_year": book.release_year,
        "title": book.title,
        "hyperlink": book.hyperlink,
        "image_hyperlink": book.image_hyperlink,
        "publisher": book.publisher,
        "description": book.description,
        "authors": [author.full_name for author in book.authors],
        "average_rating": book.average_rating
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(book) for book in books]

def review_to_dict(review: Review):
    review_dict = {
        "user_name": review.user.user_name,
        "review_id": review.book.book_id,
        "review_text": review.review_text,
        "timestamp": review.timestamp,
        "user": review.user,
    }
    return review_dict
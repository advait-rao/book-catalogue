import abc
from typing import List
from datetime import date
from collections import MutableMapping
from library.domain.model import User, Book, Review, Publisher, Author

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        """ " Adds a User to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """Returns the User named user_name from the repository.
        If there is no User given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        """Adds a given book to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book_id: int):
        """Returns a book with the given ID from the repository, else returns None"""
        raise NotImplementedError

    def get_number_of_books(self) -> int:
        """Returns the number of books in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def load_books(self, list_of_books):
        """Adds a list of books to the current list of books"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_random(self, num_books=5):
        """Returns a number of random books from the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self):
        """Returns a list of all the books in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self):
        """Returns a list of all publishers in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_publishers(self, set_of_publishers: set):
        """Adds all the publishers in a set to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_publisher(self, publisher: Publisher) -> List[Book]:
        """Returns a list of all the books published by the named publisher."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher_by_name(self, name: str) -> Publisher:
        """Returns a publisher object with the matching name."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_release_year(self, year: int) -> List[Book]:
        """Returns all books published in a given year."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_authors(self):
        """Iterates through all books in repository, and returns a list of all the authors"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_release_years(self):
        """Iterates through all books in repository, and returns a list of all the release years"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author(self, author: Author) -> List[Book]:
        """Returns all the books associated with the given author."""
        raise NotImplementedError


    def get_author_by_id(self, unique_id: int) -> Author:
        """Returns an author with the associated id."""
        raise NotImplementedError


    @abc.abstractmethod
    def add_review(self, review: Review):
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Review not correctly attached to an Book')
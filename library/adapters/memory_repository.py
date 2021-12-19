import random
import csv
from pathlib import Path
from datetime import datetime
from typing import List
from bisect import insort_left

from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import User, Book, Review, make_review, Publisher, Author
from werkzeug.security import generate_password_hash


class MemoryRepository(AbstractRepository):
    # Books ordered by ID
    def __init__(self):
        self.__users = list()
        self.__books = list()
        self.__release_years = list()
        self.__books_index = dict()
        self.__reviews = list()
        self.__publishers = list()
        self.__authors = list()
        self.__authors_index = dict()

        for book in self.__books:
            self.__release_years.append(book.release_year)
        self.__release_years = sorted(self.__release_years)

    def get_author_by_id(self, unique_id: int):
        try:
            return self.__authors_index[unique_id]
        except KeyError:
            return None

    def get_number_of_book(self) -> int:
        return len(self.__books)

    def load_authors(self):
        authors = set()
        for book in self.__books:
            for author in book.authors:
                authors.add(author)
                self.__authors_index[author.unique_id] = author
        self.__authors = list(authors)

    def get_all_authors(self) -> List[Author]:
        return self.__authors

    def get_all_release_years(self) -> List[int]:
        return self.__release_years

    def get_books_by_author(self, author: Author):
        if author in self.__authors:
            return [book for book in self.__books if author in book.authors]
        return None

    def get_book_release_year(self, year: int) -> List[Book]:
        return [book for book in self.__books if book.release_year == year]

    def get_books_by_publisher(self, the_publisher: Publisher) -> List[Book]:
        if the_publisher is None:
            the_publisher = Publisher("N/A")
        return [book for book in self.__books if book.publisher == the_publisher]

    def get_publisher_by_name(self, name: str):
        if name == "N/A":
            return None
        return next(
            (publisher for publisher in self.__publishers if publisher.name == name),
            None,
        )

    def add_publishers(self, set_of_publishers: set):
        for publisher in set_of_publishers:
            if publisher not in self.__publishers:
                self.__publishers.append(publisher)
        self.__publishers.sort()

    def get_publishers(self):
        return self.__publishers

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next(
            (user for user in self.__users if user.user_name == user_name), None
        )

    def get_book(self, book_id: int) -> Book:
        book = None
        try:
            book = self.__books_index[book_id]
        except KeyError:
            pass

        return book

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[book.book_id] = book

    def load_books(self, list_of_books):
        for book in list_of_books:
            self.add_book(book)

    def get_books_random(self, num_books=5):
        if num_books >= 100 or num_books > len(self.__books):
            num_books = min(100, self.__books)
        books = [
            self.__books[i] for i in random.sample(range(len(self.__books)), num_books)
        ]
        return books

    def get_all_books(self):
        return self.__books

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)


def read_csv_file(filename: str):
    with open(filename, encoding="utf-8-sig") as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            row = [item.strip() for item in row]
            yield row


def load_books(data_path: Path, repo: MemoryRepository):
    books_filename = str(data_path / "comic_books_excerpt.json")
    authors_filename = str(data_path / "book_authors_excerpt.json")
    reader = BooksJSONReader(books_filename, authors_filename)
    reader.read_json_files()
    repo.load_books(reader.dataset_of_books)


def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(user_name=data_row[1], password=generate_password_hash(data_row[2]))
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_publishers(repo: MemoryRepository):
    books = repo.get_all_books()
    list_of_publishers = set([book.publisher for book in books])
    repo.add_publishers(list_of_publishers)


def load_reviews(data_path: Path, repo: MemoryRepository, users):
    reviews_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(reviews_filename):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            book=repo.get_book(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4]),
        )
        repo.add_review(review)


def populate(data_path: Path, repo: MemoryRepository):
    # Load Books into the repository.
    load_books(data_path, repo)

    # Load users into repository
    users = load_users(data_path, repo)

    # Load publishers into repository
    load_publishers(repo)

    # Load authors into repository from book objects
    repo.load_authors()

    # load_reviewsss
    load_reviews(data_path, repo, users)
